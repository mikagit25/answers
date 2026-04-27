"""
LLM Provider Manager с автоматическим переключением между провайдерами.
Поддерживает: Groq, OpenRouter, Ollama (local), HuggingFace
Автоматически переключается при исчерпании лимитов или ошибках.
"""
import asyncio
import time
from typing import Optional, Dict, Any
from abc import ABC, abstractmethod
import httpx
from core.config import settings


class LLMProviderError(Exception):
    """Base exception for LLM provider errors"""
    def __init__(self, provider: str, message: str, status_code: int = None):
        self.provider = provider
        self.message = message
        self.status_code = status_code
        super().__init__(f"[{provider}] {message}")


class RateLimitError(LLMProviderError):
    """Rate limit exceeded"""
    pass


class BaseLLMProvider(ABC):
    """Abstract base class for LLM providers"""
    
    def __init__(self, name: str):
        self.name = name
        self.request_count = 0
        self.error_count = 0
        self.last_error_time = None
        self.is_disabled = False
    
    @abstractmethod
    async def generate(self, prompt: str, **kwargs) -> str:
        """Generate response from prompt"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if provider is available"""
        pass
    
    def record_success(self):
        """Record successful request"""
        self.request_count += 1
        self.error_count = 0
    
    def record_error(self, error: Exception):
        """Record failed request"""
        self.error_count += 1
        self.last_error_time = time.time()
        
        # Disable provider after too many consecutive errors
        if self.error_count >= settings.MAX_RETRIES_PER_PROVIDER:
            self.is_disabled = True


class GroqProvider(BaseLLMProvider):
    """Groq API provider (free tier: 30 req/min, 200 req/day)"""
    
    def __init__(self):
        super().__init__("groq")
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.daily_requests = 0
        self.day_start = time.time()
    
    def is_available(self) -> bool:
        if not settings.GROQ_API_KEY:
            return False
        
        if self.is_disabled:
            return False
        
        # Check daily limit (200 requests)
        if time.time() - self.day_start > 86400:  # Reset after 24 hours
            self.daily_requests = 0
            self.day_start = time.time()
        
        if self.daily_requests >= 200:
            return False
        
        return True
    
    async def generate(self, prompt: str, **kwargs) -> str:
        if not self.is_available():
            raise LLMProviderError(self.name, "Provider not available")
        
        headers = {
            "Authorization": f"Bearer {settings.GROQ_API_KEY}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "model": settings.GROQ_MODEL,
            "messages": [
                {"role": "system", "content": kwargs.get("system_prompt", "")},
                {"role": "user", "content": prompt}
            ],
            "temperature": kwargs.get("temperature", 0.3),
            "max_tokens": kwargs.get("max_tokens", 500),
        }
        
        try:
            async with httpx.AsyncClient(timeout=settings.REQUEST_TIMEOUT) as client:
                response = await client.post(self.base_url, json=payload, headers=headers)
                
                if response.status_code == 429:
                    self.daily_requests += 1
                    raise RateLimitError(self.name, "Rate limit exceeded", 429)
                
                response.raise_for_status()
                data = response.json()
                
                self.record_success()
                self.daily_requests += 1
                
                return data["choices"][0]["message"]["content"]
                
        except httpx.HTTPStatusError as e:
            self.record_error(e)
            if e.response.status_code == 429:
                raise RateLimitError(self.name, "Rate limit exceeded", 429)
            raise LLMProviderError(self.name, f"HTTP error: {e.response.status_code}", e.response.status_code)
        except Exception as e:
            self.record_error(e)
            raise LLMProviderError(self.name, f"Request failed: {str(e)}")


class OpenRouterProvider(BaseLLMProvider):
    """OpenRouter provider with free models"""
    
    def __init__(self):
        super().__init__("openrouter")
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
    
    def is_available(self) -> bool:
        if not settings.OPENROUTER_API_KEY:
            return False
        
        return not self.is_disabled
    
    async def generate(self, prompt: str, **kwargs) -> str:
        if not self.is_available():
            raise LLMProviderError(self.name, "Provider not available")
        
        headers = {
            "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/mikagit25/answers",
            "X-Title": "Answers Platform",
        }
        
        payload = {
            "model": settings.OPENROUTER_MODEL,
            "messages": [
                {"role": "system", "content": kwargs.get("system_prompt", "")},
                {"role": "user", "content": prompt}
            ],
            "temperature": kwargs.get("temperature", 0.3),
            "max_tokens": kwargs.get("max_tokens", 500),
        }
        
        try:
            async with httpx.AsyncClient(timeout=settings.REQUEST_TIMEOUT) as client:
                response = await client.post(self.base_url, json=payload, headers=headers)
                
                if response.status_code == 429:
                    raise RateLimitError(self.name, "Rate limit exceeded", 429)
                
                response.raise_for_status()
                data = response.json()
                
                self.record_success()
                return data["choices"][0]["message"]["content"]
                
        except httpx.HTTPStatusError as e:
            self.record_error(e)
            if e.response.status_code == 429:
                raise RateLimitError(self.name, "Rate limit exceeded", 429)
            raise LLMProviderError(self.name, f"HTTP error: {e.response.status_code}", e.response.status_code)
        except Exception as e:
            self.record_error(e)
            raise LLMProviderError(self.name, f"Request failed: {str(e)}")


class OllamaProvider(BaseLLMProvider):
    """Local Ollama provider (completely free, no limits)"""
    
    def __init__(self):
        super().__init__("ollama")
        self.base_url = f"{settings.OLLAMA_BASE_URL}/api/generate"
    
    def is_available(self) -> bool:
        if self.is_disabled:
            return False
        
        # Check if Ollama is running
        try:
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('localhost', 11434))
            sock.close()
            return result == 0
        except:
            return False
    
    async def generate(self, prompt: str, **kwargs) -> str:
        if not self.is_available():
            raise LLMProviderError(self.name, "Ollama not running on localhost:11434")
        
        payload = {
            "model": settings.OLLAMA_MODEL,
            "prompt": f"{kwargs.get('system_prompt', '')}\n\n{prompt}",
            "stream": False,
            "options": {
                "temperature": kwargs.get("temperature", 0.3),
                "num_predict": kwargs.get("max_tokens", 500),
            }
        }
        
        try:
            async with httpx.AsyncClient(timeout=settings.REQUEST_TIMEOUT) as client:
                response = await client.post(self.base_url, json=payload)
                response.raise_for_status()
                data = response.json()
                
                self.record_success()
                return data["response"]
                
        except httpx.HTTPError as e:
            self.record_error(e)
            raise LLMProviderError(self.name, f"Ollama request failed: {str(e)}")
        except Exception as e:
            self.record_error(e)
            raise LLMProviderError(self.name, f"Request failed: {str(e)}")


class HuggingFaceProvider(BaseLLMProvider):
    """Hugging Face Inference API (free tier)"""
    
    def __init__(self):
        super().__init__("huggingface")
        self.base_url = f"https://api-inference.huggingface.co/models/{settings.HUGGINGFACE_MODEL}"
    
    def is_available(self) -> bool:
        if not settings.HUGGINGFACE_API_KEY:
            return False
        
        return not self.is_disabled
    
    async def generate(self, prompt: str, **kwargs) -> str:
        if not self.is_available():
            raise LLMProviderError(self.name, "Provider not available")
        
        headers = {
            "Authorization": f"Bearer {settings.HUGGINGFACE_API_KEY}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "inputs": f"{kwargs.get('system_prompt', '')}\n\nUser: {prompt}\nAssistant:",
            "parameters": {
                "max_new_tokens": kwargs.get("max_tokens", 500),
                "temperature": kwargs.get("temperature", 0.3),
                "return_full_text": False,
            }
        }
        
        try:
            async with httpx.AsyncClient(timeout=settings.REQUEST_TIMEOUT) as client:
                response = await client.post(self.base_url, json=payload, headers=headers)
                
                if response.status_code == 503:
                    raise LLMProviderError(self.name, "Model loading, try again later", 503)
                
                if response.status_code == 429:
                    raise RateLimitError(self.name, "Rate limit exceeded", 429)
                
                response.raise_for_status()
                data = response.json()
                
                self.record_success()
                return data[0]["generated_text"]
                
        except httpx.HTTPStatusError as e:
            self.record_error(e)
            if e.response.status_code == 429:
                raise RateLimitError(self.name, "Rate limit exceeded", 429)
            raise LLMProviderError(self.name, f"HTTP error: {e.response.status_code}", e.response.status_code)
        except Exception as e:
            self.record_error(e)
            raise LLMProviderError(self.name, f"Request failed: {str(e)}")


class QwenProvider(BaseLLMProvider):
    """
    Qwen API Provider (Self-hosted or Alibaba Cloud)
    Supports OpenAI-compatible API format for easy integration.
    Can be shared across multiple projects simultaneously.
    """
    
    def __init__(self):
        super().__init__("qwen")
        # Remove trailing /v1 if present, then add /chat/completions
        base = settings.QWEN_API_BASE_URL.rstrip('/')
        if base.endswith('/v1'):
            self.base_url = f"{base}/chat/completions"
        else:
            self.base_url = f"{base}/chat/completions"
    
    def is_available(self) -> bool:
        # Check if base URL is configured
        if not settings.QWEN_API_BASE_URL:
            return False
        
        if self.is_disabled:
            return False
        
        # Try to ping the server
        try:
            import socket
            from urllib.parse import urlparse
            parsed = urlparse(settings.QWEN_API_BASE_URL)
            host = parsed.hostname or 'localhost'
            port = parsed.port or (443 if parsed.scheme == 'https' else 80)
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except:
            return False
    
    async def generate(self, prompt: str, **kwargs) -> str:
        if not self.is_available():
            raise LLMProviderError(self.name, "Qwen server not available")
        
        headers = {
            "Content-Type": "application/json",
        }
        
        # Add API key if configured
        if settings.QWEN_API_KEY:
            headers["Authorization"] = f"Bearer {settings.QWEN_API_KEY}"
        
        payload = {
            "model": settings.QWEN_MODEL,
            "messages": [
                {"role": "system", "content": kwargs.get("system_prompt", "")},
                {"role": "user", "content": prompt}
            ],
            "temperature": kwargs.get("temperature", 0.3),
            "max_tokens": kwargs.get("max_tokens", 500),
        }
        
        try:
            async with httpx.AsyncClient(timeout=settings.REQUEST_TIMEOUT) as client:
                response = await client.post(self.base_url, json=payload, headers=headers)
                
                if response.status_code == 429:
                    raise RateLimitError(self.name, "Rate limit exceeded", 429)
                
                if response.status_code == 503:
                    raise LLMProviderError(self.name, "Service unavailable", 503)
                
                response.raise_for_status()
                data = response.json()
                
                self.record_success()
                return data["choices"][0]["message"]["content"]
                
        except httpx.HTTPStatusError as e:
            self.record_error(e)
            if e.response.status_code == 429:
                raise RateLimitError(self.name, "Rate limit exceeded", 429)
            raise LLMProviderError(self.name, f"HTTP error: {e.response.status_code}", e.response.status_code)
        except httpx.ConnectError as e:
            self.record_error(e)
            raise LLMProviderError(self.name, f"Cannot connect to Qwen server: {str(e)}")
        except Exception as e:
            self.record_error(e)
            raise LLMProviderError(self.name, f"Request failed: {str(e)}")


class LLMProviderManager:
    """
    Manager для управления несколькими LLM провайдерами с автоматическим fallback.
    Пробует провайдеров по порядку приоритета.
    """
    
    def __init__(self):
        self.providers: Dict[str, BaseLLMProvider] = {
            "groq": GroqProvider(),
            "openrouter": OpenRouterProvider(),
            "qwen": QwenProvider(),
            "ollama": OllamaProvider(),
            "huggingface": HuggingFaceProvider(),
        }
        self.current_provider_index = 0
        self.provider_stats = {
            name: {"successes": 0, "failures": 0, "last_used": None}
            for name in self.providers.keys()
        }
    
    def get_available_providers(self) -> list:
        """Get list of available providers in priority order"""
        available = []
        for provider_name in settings.LLM_PROVIDER_PRIORITY:
            if provider_name in self.providers:
                provider = self.providers[provider_name]
                if provider.is_available():
                    available.append(provider_name)
        return available
    
    async def generate_with_fallback(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """
        Generate response with automatic fallback to next provider on failure.
        Returns response and metadata about which provider was used.
        """
        available_providers = self.get_available_providers()
        
        if not available_providers:
            raise LLMProviderError("all", "No LLM providers available. Please configure at least one API key or start Ollama.")
        
        last_error = None
        
        for provider_name in available_providers:
            provider = self.providers[provider_name]
            
            try:
                print(f"🤖 Using LLM provider: {provider_name}")
                response = await provider.generate(prompt, **kwargs)
                
                # Update stats
                self.provider_stats[provider_name]["successes"] += 1
                self.provider_stats[provider_name]["last_used"] = time.time()
                
                return {
                    "response": response,
                    "provider": provider_name,
                    "model": self._get_model_name(provider_name),
                    "fallback_used": len(available_providers) > 1,
                }
                
            except RateLimitError as e:
                print(f"⚠️  Rate limit hit for {provider_name}, switching to next provider...")
                self.provider_stats[provider_name]["failures"] += 1
                last_error = e
                continue
                
            except LLMProviderError as e:
                print(f"❌ Error with {provider_name}: {e.message}")
                self.provider_stats[provider_name]["failures"] += 1
                last_error = e
                continue
        
        # All providers failed
        raise LLMProviderError("all", f"All providers failed. Last error: {str(last_error)}")
    
    def _get_model_name(self, provider_name: str) -> str:
        """Get model name for provider"""
        model_map = {
            "groq": settings.GROQ_MODEL,
            "openrouter": settings.OPENROUTER_MODEL,
            "qwen": settings.QWEN_MODEL,
            "ollama": settings.OLLAMA_MODEL,
            "huggingface": settings.HUGGINGFACE_MODEL,
        }
        return model_map.get(provider_name, "unknown")
    
    def get_stats(self) -> Dict:
        """Get provider usage statistics"""
        return {
            "stats": self.provider_stats,
            "available_providers": self.get_available_providers(),
            "current_priority_order": settings.LLM_PROVIDER_PRIORITY,
        }
    
    def reset_provider(self, provider_name: str):
        """Manually reset a disabled provider"""
        if provider_name in self.providers:
            self.providers[provider_name].is_disabled = False
            self.providers[provider_name].error_count = 0
            print(f"✅ Provider '{provider_name}' has been reset")


# Global instance
llm_manager = LLMProviderManager()
