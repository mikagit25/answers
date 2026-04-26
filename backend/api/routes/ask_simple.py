"""
Упрощенная версия роута ask для работы с SQLite.
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from db.connection_sqlite import get_db
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
    db: Session = None  # SQLite doesn't need async session
):
    """
    Получение ответа на вопрос в рамках выбранной традиции.
    
    - **question**: Текст вопроса (10-500 символов)
    - **tradition_id**: ID выбранной традиции
    - **depth**: Глубина ответа (basic/advanced)
    """
    start_time = time.time()
    
    try:
        print(f"\n📨 Received question: {request.question[:50]}...")
        print(f"🎯 Tradition: {request.tradition_id}")
        
        # Обработка вопроса через RAG pipeline
        result = await rag_pipeline.process_question(
            session=None,  # SQLite version will handle DB differently
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
        
        print(f"✅ Response generated in {response_time}ms")
        print(f"📊 Sources found: {result.get('metadata', {}).get('total_sources_found', 0)}")
        
        response = AskResponse(
            answer=result["answer"],
            sources=[SourceResponse(**src) for src in result["sources"]],
            tradition_id=result["tradition_id"],
            share_url=share_url,
            status=result["status"],
            metadata={
                "response_time_ms": response_time,
                "cache_hit": False,
                **result.get("metadata", {})
            }
        )
        
        return response
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {str(e)}")


def generate_share_slug(question: str, tradition_id: str) -> str:
    """Генерация slug для URL шаринга"""
    hash_input = f"{question.lower().strip()}-{tradition_id}"
    short_hash = hashlib.md5(hash_input.encode()).hexdigest()[:8]
    
    words = question.lower().split()[:3]
    slug_words = []
    for word in words:
        cleaned = ''.join(c for c in word if c.isalnum())
        if cleaned:
            slug_words.append(cleaned)
    
    slug_base = "-".join(slug_words) if slug_words else "question"
    return f"{tradition_id}-{slug_base}-{short_hash}"
