"""
Middleware для безопасности: rate limiting, валидация запросов.
"""
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import time
import hashlib
from core.config import settings

# In-memory rate limiting (use Redis in production)
rate_limit_store = {}


class RateLimiter:
    """Простой rate limiter на основе IP"""
    
    def __init__(self, max_requests: int = 60, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
    
    def is_rate_limited(self, client_id: str) -> bool:
        current_time = time.time()
        
        if client_id not in rate_limit_store:
            rate_limit_store[client_id] = []
        
        # Очистка старых запросов
        rate_limit_store[client_id] = [
            timestamp for timestamp in rate_limit_store[client_id]
            if current_time - timestamp < self.window_seconds
        ]
        
        # Проверка лимита
        if len(rate_limit_store[client_id]) >= self.max_requests:
            return True
        
        # Добавление текущего запроса
        rate_limit_store[client_id].append(current_time)
        return False


# Global rate limiter instance
rate_limiter = RateLimiter(max_requests=60, window_seconds=60)


async def rate_limit_middleware(request: Request, call_next):
    """Middleware для ограничения частоты запросов"""
    # Получение идентификатора клиента (IP или API key)
    client_ip = request.client.host if request.client else "unknown"
    client_id = hashlib.md5(client_ip.encode()).hexdigest()
    
    if rate_limiter.is_rate_limited(client_id):
        return JSONResponse(
            status_code=429,
            content={"detail": "Слишком много запросов. Попробуйте позже."}
        )
    
    response = await call_next(request)
    return response


def validate_question_text(question: str) -> bool:
    """Валидация текста вопроса на безопасность"""
    # Проверка длины
    if len(question) < 10 or len(question) > 500:
        return False
    
    # Проверка на потенциально вредоносные паттерны
    forbidden_patterns = [
        '<script',
        'javascript:',
        'onerror=',
        'onclick=',
    ]
    
    question_lower = question.lower()
    for pattern in forbidden_patterns:
        if pattern in question_lower:
            return False
    
    return True


def sanitize_input(text: str) -> str:
    """Очистка пользовательского ввода"""
    # Удаление потенциально опасных символов
    sanitized = text.strip()
    
    # Ограничение длины
    if len(sanitized) > 500:
        sanitized = sanitized[:500]
    
    return sanitized
