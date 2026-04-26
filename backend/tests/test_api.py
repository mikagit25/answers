"""
Тесты для API endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_check():
    """Тест health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_ask_question_validation():
    """Тест валидации запроса вопроса"""
    # Тест на пустой вопрос
    response = client.post("/api/v1/ask", json={
        "question": "",
        "tradition_id": "stoicism"
    })
    assert response.status_code == 422
    
    # Тест на слишком короткий вопрос
    response = client.post("/api/v1/ask", json={
        "question": "Short",
        "tradition_id": "stoicism"
    })
    assert response.status_code == 422
    
    # Тест на отсутствие традиции
    response = client.post("/api/v1/ask", json={
        "question": "This is a valid question with enough length"
    })
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_compare_traditions():
    """Тест сравнения традиций"""
    response = client.get("/api/v1/compare", params={
        "question": "What is the meaning of life?"
    })
    # Пока возвращает заглушки, но должен быть 200
    assert response.status_code == 200
