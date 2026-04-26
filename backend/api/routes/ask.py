"""
API роут для обработки вопросов пользователей.
POST /api/v1/ask - получение ответа на вопрос в рамках выбранной традиции
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from db.connection import get_db
from api.schemas import AskRequest, AskResponse, SourceResponse
from rag.pipeline import RAGPipeline
import time
import hashlib

router = APIRouter()
rag_pipeline = RAGPipeline()


@router.post("/", response_model=AskResponse)
async def ask_question(
    request: AskRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """
    Получение ответа на вопрос в рамках выбранной традиции.
    
    - **question**: Текст вопроса (10-500 символов)
    - **tradition_id**: ID выбранной традиции
    - **depth**: Глубина ответа (basic/advanced)
    """
    start_time = time.time()
    
    try:
        # Обработка вопроса через RAG pipeline
        result = await rag_pipeline.process_question(
            session=db,
            question=request.question,
            tradition_id=request.tradition_id
        )
        
        # Проверка статуса
        if result["status"] == "no_sources":
            raise HTTPException(
                status_code=404,
                detail="Недостаточно источников для ответа на этот вопрос в данной традиции"
            )
        
        # Генерация URL для шаринга
        share_slug = generate_share_slug(request.question, request.tradition_id)
        share_url = f"/answer/{share_slug}"
        
        # Формирование ответа
        response_time = int((time.time() - start_time) * 1000)
        
        response = AskResponse(
            answer=result["answer"],
            sources=[SourceResponse(**src) for src in result["sources"]],
            tradition_id=result["tradition_id"],
            share_url=share_url,
            status=result["status"],
            metadata={
                "model": "qwen-turbo",
                "response_time_ms": response_time,
                "cache_hit": False,  # TODO: implement caching
                **result.get("metadata", {})
            }
        )
        
        # Фоновая задача: сохранение запроса в историю (опционально)
        background_tasks.add_task(
            save_query_to_history,
            question=request.question,
            tradition_id=request.tradition_id,
            response_time_ms=response_time
        )
        
        return response
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {str(e)}")


def generate_share_slug(question: str, tradition_id: str) -> str:
    """Генерация slug для URL шаринга"""
    # Создание короткого хэша из вопроса и традиции
    hash_input = f"{question.lower().strip()}-{tradition_id}"
    short_hash = hashlib.md5(hash_input.encode()).hexdigest()[:8]
    
    # Транслитерация первых слов вопроса
    words = question.lower().split()[:3]
    slug_words = []
    for word in words:
        # Удаление специальных символов
        cleaned = ''.join(c for c in word if c.isalnum())
        if cleaned:
            slug_words.append(cleaned)
    
    slug_base = "-".join(slug_words) if slug_words else "question"
    return f"{tradition_id}-{slug_base}-{short_hash}"


async def save_query_to_history(
    question: str,
    tradition_id: str,
    response_time_ms: int
):
    """
    Фоновая задача для сохранения запроса в историю.
    TODO: реализовать сохранение в БД
    """
    pass
