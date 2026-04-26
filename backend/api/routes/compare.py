"""
API роут для сравнения ответов разных традиций.
GET /api/v1/compare - получение сравнительного анализа
"""
from fastapi import APIRouter, Query, HTTPException
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from db.connection import get_db
from api.schemas import CompareResponse, TraditionComparison

router = APIRouter()


@router.get("/", response_model=CompareResponse)
async def compare_traditions(
    question: str = Query(..., min_length=10, max_length=500, description="Текст вопроса"),
    exclude: Optional[str] = Query(None, description="ID традиции для исключения"),
    db: AsyncSession = Depends(get_db)
):
    """
    Сравнение подходов разных традиций к одному вопросу.
    
    - **question**: Текст вопроса для сравнения
    - **exclude**: ID традиции, которую нужно исключить из сравнения
    """
    try:
        # Получение списка активных традиций (исключая указанную)
        query = text("""
            SELECT id, name, description 
            FROM traditions 
            WHERE is_active = true
        """)
        
        if exclude:
            query = text("""
                SELECT id, name, description 
                FROM traditions 
                WHERE is_active = true AND id != :exclude
                LIMIT 3
            """)
            result = await db.execute(query, {"exclude": exclude})
        else:
            query = text("""
                SELECT id, name, description 
                FROM traditions 
                WHERE is_active = true
                LIMIT 4
            """)
            result = await db.execute(query)
        
        traditions = [
            {"id": row.id, "name": row.name, "description": row.description}
            for row in result
        ]
        
        if not traditions:
            raise HTTPException(status_code=404, detail="Нет доступных традиций для сравнения")
        
        # TODO: Здесь должна быть логика генерации сравнений через LLM
        # Для сейчас возвращаем заглушки
        comparisons = []
        for tradition in traditions:
            comparisons.append(TraditionComparison(
                tradition_id=tradition["id"],
                tradition_name=tradition["name"],
                summary=f"В рамках традиции {tradition['name']} этот вопрос рассматривается через призму их основных принципов. (Заглушка - требуется реализация)",
                source_preview="Источник будет добавлен после полной реализации RAG pipeline"
            ))
        
        return CompareResponse(comparisons=comparisons)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при сравнении: {str(e)}")
