"""
Pydantic схемы для валидации запросов и ответов API.
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict


class AskRequest(BaseModel):
    """Запрос на получение ответа"""
    question: str = Field(..., min_length=10, max_length=500, description="Текст вопроса")
    tradition_id: str = Field(..., description="ID выбранной традиции")
    depth: str = Field(default="basic", description="Глубина ответа (basic/advanced)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "Как преодолеть страх перед будущим?",
                "tradition_id": "stoicism",
                "depth": "basic"
            }
        }


class SourceResponse(BaseModel):
    """Информация об источнике"""
    text: str
    reference: str
    translation: str
    commentary: str


class AskResponse(BaseModel):
    """Ответ API на вопрос пользователя"""
    answer: str
    sources: List[SourceResponse]
    tradition_id: str
    share_url: Optional[str] = None
    status: str = "success"
    metadata: Optional[Dict] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "answer": "В стоицизме страх перед будущим преодолевается через...",
                "sources": [
                    {
                        "text": "«Люди страдают не от вещей, а от мнений о вещах»",
                        "reference": "Эпиктет, Энхиридион, §5",
                        "translation": "пер. С. Соболевского",
                        "commentary": "Адаптация для современного читателя"
                    }
                ],
                "tradition_id": "stoicism",
                "share_url": "/answer/stoicism-fear-future-a1b2c3",
                "status": "success",
                "metadata": {"model": "qwen-turbo", "tokens": 380, "cache_hit": False}
            }
        }


class CompareRequest(BaseModel):
    """Запрос на сравнение традиций"""
    question: str = Field(..., min_length=10, max_length=500)
    exclude: Optional[str] = Field(None, description="ID традиции для исключения из сравнения")


class TraditionComparison(BaseModel):
    """Результат сравнения одной традиции"""
    tradition_id: str
    tradition_name: str
    summary: str
    source_preview: str


class CompareResponse(BaseModel):
    """Ответ API с сравнением традиций"""
    comparisons: List[TraditionComparison]


class FeedbackRequest(BaseModel):
    """Обратная связь по ответу"""
    question: str
    tradition_id: str
    feedback_type: str  # "accurate", "clarify_source", "suggest_tradition"
    comment: Optional[str] = None
