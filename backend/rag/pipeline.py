"""
RAG конвейер: загрузка, эмбеддинг, ретривер, генератор ответов.
Использует гибридный поиск (векторный + BM25) и пост-валидацию источников.
Теперь использует LLM Provider Manager с автоматическим fallback.
"""
import hashlib
import json
from typing import List, Dict, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from langchain_community.embeddings import HuggingFaceEmbeddings
from core.config import settings
from rag.prompts import TRADITION_PROMPTS
from rag.validator import validate_sources
from core.llm_manager import llm_manager


class RAGPipeline:
    """Основной класс RAG конвейера"""
    
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL
        )
        
    async def retrieve_context(
        self, 
        session: AsyncSession, 
        question: str, 
        tradition_id: str,
        top_k: int = None
    ) -> List[Dict]:
        """
        Извлечение релевантного контекста из БД с использованием векторного поиска.
        Возвращает список источников с метаданными.
        """
        if top_k is None:
            top_k = settings.TOP_K_RETRIEVAL
        
        # Генерация эмбеддинга вопроса
        question_embedding = self.embeddings.embed_query(question)
        
        # Векторный поиск с фильтрацией по традиции
        query = text("""
            SELECT 
                s.id as source_id,
                s.author,
                s.work,
                s.section,
                s.text,
                s.translation,
                s.commentary,
                s.tags,
                c.embedding <-> :embedding as similarity
            FROM chunks c
            JOIN sources s ON c.source_id = s.id
            WHERE s.tradition_id = :tradition_id
            ORDER BY c.embedding <-> :embedding
            LIMIT :limit
        """)
        
        result = await session.execute(query, {
            'embedding': json.dumps(question_embedding),
            'tradition_id': tradition_id,
            'limit': top_k
        })
        
        sources = []
        for row in result:
            sources.append({
                'source_id': row.source_id,
                'author': row.author,
                'work': row.work,
                'section': row.section,
                'text': row.text,
                'translation': row.translation,
                'commentary': row.commentary,
                'tags': row.tags,
                'similarity': row.similarity,
            })
        
        return sources
    
    def format_context(self, sources: List[Dict]) -> str:
        """Форматирование источников в контекст для промпта"""
        context_parts = []
        for i, source in enumerate(sources, 1):
            section_info = f", {source['section']}" if source['section'] else ""
            translation_info = f" (пер. {source['translation']})" if source['translation'] else ""
            
            context_parts.append(
                f"[{i}] {source['author']}, {source['work']}{section_info}{translation_info}:\n"
                f"\"{source['text']}\"\n"
            )
        
        return "\n".join(context_parts)
    
    async def generate_answer(
        self, 
        question: str, 
        tradition_id: str, 
        sources: List[Dict]
    ) -> Tuple[str, List[Dict], Dict]:
        """
        Генерация ответа на основе вопроса и найденных источников.
        Использует LLM Provider Manager с автоматическим fallback.
        Возвращает ответ, валидированные источники и метаданные.
        """
        # Форматирование контекста
        context = self.format_context(sources)
        
        # Получение промпта для традиции
        prompt_template = TRADITION_PROMPTS.get(tradition_id)
        if not prompt_template:
            raise ValueError(f"Неизвестная традиция: {tradition_id}")
        
        # Подготовка промпта
        system_prompt = "Ты эксперт по философским и религиозным традициям."
        user_prompt = prompt_template.format(context=context, question=question)
        
        # Генерация ответа через LLM Manager с fallback
        llm_result = await llm_manager.generate_with_fallback(
            prompt=user_prompt,
            system_prompt=system_prompt,
            temperature=0.3,
            max_tokens=500,
        )
        
        answer = llm_result["response"]
        
        # Пост-валидация источников
        validated_sources = validate_sources(answer, sources)
        
        # Метаданные о использованном провайдере
        provider_metadata = {
            "llm_provider": llm_result["provider"],
            "llm_model": llm_result["model"],
            "fallback_used": llm_result["fallback_used"],
        }
        
        return answer, validated_sources, provider_metadata
    
    def generate_cache_key(self, question: str, tradition_id: str) -> str:
        """Генерация ключа для кэширования"""
        cache_string = f"{question.lower().strip()}|{tradition_id}"
        return hashlib.sha256(cache_string.encode()).hexdigest()
    
    async def process_question(
        self, 
        session: AsyncSession, 
        question: str, 
        tradition_id: str
    ) -> Dict:
        """
        Полный цикл обработки вопроса: поиск, генерация, валидация.
        Возвращает структурированный ответ.
        """
        # Шаг 1: Извлечение контекста
        sources = await self.retrieve_context(session, question, tradition_id)
        
        if not sources:
            return {
                "answer": "К сожалению, в рамках данной традиции недостаточно информации для ответа на этот вопрос.",
                "sources": [],
                "status": "no_sources",
            }
        
        # Шаг 2: Генерация ответа с автоматическим fallback
        answer, validated_sources, provider_metadata = await self.generate_answer(
            question, tradition_id, sources
        )
        
        # Шаг 3: Проверка статуса
        status = "success" if len(validated_sources) >= 2 else "uncertain"
        
        # Форматирование источников для ответа
        formatted_sources = []
        for source in validated_sources[:4]:  # Максимум 4 источника
            section_info = f", {source['section']}" if source['section'] else ""
            translation_info = f" (пер. {source['translation']})" if source['translation'] else ""
            commentary_info = f"\nКомментарий: {source['commentary']}" if source['commentary'] else ""
            
            formatted_sources.append({
                "text": source['text'],
                "reference": f"{source['author']}, {source['work']}{section_info}",
                "translation": source['translation'] or "оригинал",
                "commentary": source['commentary'] or "",
            })
        
        return {
            "answer": answer,
            "sources": formatted_sources,
            "tradition_id": tradition_id,
            "status": status,
            "metadata": {
                "total_sources_found": len(sources),
                "validated_sources": len(validated_sources),
                **provider_metadata,  # Добавляем информацию о провайдере
            }
        }
