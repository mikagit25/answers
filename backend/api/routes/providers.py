"""
API роут для проверки статуса LLM провайдеров.
GET /api/v1/providers/status - получение информации о доступных провайдерах
POST /api/v1/providers/reset - сброс отключенного провайдера
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from core.llm_manager import llm_manager

router = APIRouter()


class ResetProviderRequest(BaseModel):
    provider_name: str


@router.get("/status")
async def get_providers_status():
    """Получить статус всех LLM провайдеров"""
    try:
        stats = llm_manager.get_stats()
        return {
            "status": "success",
            "data": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reset")
async def reset_provider(request: ResetProviderRequest):
    """Сбросить отключенный провайдер"""
    try:
        if request.provider_name not in llm_manager.providers:
            raise HTTPException(
                status_code=404,
                detail=f"Unknown provider: {request.provider_name}"
            )
        
        llm_manager.reset_provider(request.provider_name)
        return {
            "status": "success",
            "message": f"Provider '{request.provider_name}' has been reset"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
