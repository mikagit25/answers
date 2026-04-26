"""
Скрипт для импорта данных из knowledge_base в PostgreSQL с генерацией эмбеддингов.
Использование: python ingest.py
"""
import asyncio
import json
import os
from pathlib import Path
from typing import List, Dict
from sentence_transformers import SentenceTransformer
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import Tradition, Source, Chunk
from db.connection import AsyncSessionLocal, init_db
from core.config import settings


class DataIngestor:
    """Класс для импорта данных о традициях и источниках"""
    
    def __init__(self):
        self.embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)
        self.knowledge_base_path = Path(__file__).parent.parent / "knowledge_base"
        
    async def load_traditions(self) -> List[Dict]:
        """Загрузка метаданных традиций"""
        metadata_file = self.knowledge_base_path / "metadata.json"
        with open(metadata_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get('traditions', [])
    
    async def load_sources_for_tradition(self, tradition_id: str) -> List[Dict]:
        """Загрузка источников для конкретной традиции"""
        source_file = self.knowledge_base_path / "traditions" / f"{tradition_id}.json"
        if not source_file.exists():
            print(f"⚠️  Файл не найден: {source_file}")
            return []
        
        with open(source_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get('sources', [])
    
    def chunk_text(self, text: str, chunk_size: int = None, overlap: int = None) -> List[str]:
        """Разбиение текста на чанки с перекрытием"""
        if chunk_size is None:
            chunk_size = settings.CHUNK_SIZE
        if overlap is None:
            overlap = settings.CHUNK_OVERLAP
            
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk = ' '.join(words[i:i + chunk_size])
            if chunk:
                chunks.append(chunk)
        
        return chunks if chunks else [text]
    
    async def ingest_tradition(self, session: AsyncSession, tradition_data: Dict):
        """Импорт одной традиции и её источников"""
        tradition_id = tradition_data['id']
        print(f"\n📚 Обработка традиции: {tradition_data['name']}")
        
        # Создание или обновление традиции
        tradition = Tradition(
            id=tradition_id,
            name=tradition_data['name'],
            description=tradition_data.get('description'),
            icon=tradition_data.get('icon'),
            color=tradition_data.get('color'),
        )
        session.add(tradition)
        await session.flush()
        
        # Загрузка источников
        sources = await self.load_sources_for_tradition(tradition_id)
        print(f"   Найдено источников: {len(sources)}")
        
        for source_data in sources:
            source = Source(
                id=source_data['id'],
                tradition_id=tradition_id,
                author=source_data['author'],
                work=source_data['work'],
                section=source_data.get('section'),
                text=source_data['text'],
                translation=source_data.get('translation'),
                commentary=source_data.get('commentary'),
                tags=','.join(source_data.get('tags', [])),
            )
            session.add(source)
            await session.flush()
            
            # Создание чанков и генерация эмбеддингов
            chunks = self.chunk_text(source_data['text'])
            for i, chunk_text in enumerate(chunks):
                embedding = self.embedding_model.encode(chunk_text).tolist()
                
                chunk = Chunk(
                    source_id=source.id,
                    content=chunk_text,
                    embedding=embedding,
                    metadata_json=json.dumps({
                        'chunk_index': i,
                        'total_chunks': len(chunks),
                        'tradition_id': tradition_id,
                    }),
                )
                session.add(chunk)
            
            print(f"   ✓ Источник: {source_data['author']} - {source_data['work']}")
        
        await session.commit()
        print(f"✅ Традиция '{tradition_data['name']}' успешно импортирована")
    
    async def run(self):
        """Запуск процесса импорта"""
        print("🚀 Начало импорта данных...\n")
        
        # Инициализация БД
        await init_db()
        print("✓ База данных инициализирована")
        
        # Загрузка традиций
        traditions = await self.load_traditions()
        print(f"Найдено традиций: {len(traditions)}\n")
        
        # Импорт каждой традиции
        async with AsyncSessionLocal() as session:
            for tradition_data in traditions:
                try:
                    await self.ingest_tradition(session, tradition_data)
                except Exception as e:
                    print(f"❌ Ошибка импорта традиции {tradition_data['id']}: {e}")
                    await session.rollback()
        
        print("\n🎉 Импорт завершён!")


async def main():
    ingestor = DataIngestor()
    await ingestor.run()


if __name__ == "__main__":
    asyncio.run(main())
