"""
RAG конвейер: загрузка, эмбеддинг, ретривер, генератор ответов.
Использует гибридный поиск (векторный + BM25) и пост-валидацию источников.
"""
import hashlib
import json
from typing import List, Dict, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import PGVector
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from core.config import settings
from rag.prompts import TRADITION_PROMPTS
from rag.validator import validate_sources


class RAGPipeline:
    """Основной класс RAG конвейера"""
    
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL
        )
        self.llm = ChatOpenAI(
            openai_api_key=settings.QWEN_API_KEY,
            openai_api_base="https://openrouter.ai/api/v1",  # или прямой API Qwen
            model_name="qwen/qwen-turbo",
            temperature=0.3,
            max_tokens=500,
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
    ) -> Tuple[str, List[Dict]]:
        """
        Генерация ответа на основе вопроса и найденных источников.
        Возвращает ответ и валидированные источники.
        """
        # Форматирование контекста
        context = self.format_context(sources)
        
        # Получение промпта для традиции
        prompt_template = TRADITION_PROMPTS.get(tradition_id)
        if not prompt_template:
            raise ValueError(f"Неизвестная традиция: {tradition_id}")
        
        # Создание промпта
        prompt = PromptTemplate(
            input_variables=["context", "question"],
            template=prompt_template
        )
        
        # Генерация ответа
        chain = LLMChain(llm=self.llm, prompt=prompt)
        result = await chain.arun(context=context, question=question)
        
        # Пост-валидация источников
        validated_sources = validate_sources(result, sources)
        
        return result, validated_sources
    
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
        
        # Шаг 2: Генерация ответа
        answer, validated_sources = await self.generate_answer(
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
            }
        }
