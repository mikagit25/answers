"""
Модуль для автоматической генерации SEO-статей на основе пользовательских запросов.
Собирает популярные вопросы, агрегирует ответы и создает полноценные статьи.
"""
import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path
import hashlib


class ArticleGenerator:
    """Генератор SEO-статей из пользовательских диалогов."""
    
    def __init__(self, articles_dir: str = "articles"):
        self.articles_dir = Path(articles_dir)
        self.questions_db_path = Path("data/user_questions.json")
        self.generated_articles_path = Path("data/generated_articles.json")
        
        # Создаем директории если не существуют
        self.articles_dir.mkdir(parents=True, exist_ok=True)
        self.questions_db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Загружаем или создаем базу вопросов
        self.questions_db = self._load_questions_db()
        self.generated_articles = self._load_generated_articles()
    
    def _load_questions_db(self) -> Dict:
        """Загружает базу пользовательских вопросов."""
        if self.questions_db_path.exists():
            with open(self.questions_db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "questions": [],
            "topics": {},
            "last_updated": datetime.now().isoformat()
        }
    
    def _load_generated_articles(self) -> Dict:
        """Загружает информацию о сгенерированных статьях."""
        if self.generated_articles_path.exists():
            with open(self.generated_articles_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"articles": [], "last_generated": None}
    
    def save_question(self, question: str, tradition_id: str, answer: str, 
                     language: str = "ru", depth: str = "basic",
                     conversation_id: Optional[str] = None):
        """Сохраняет пользовательский вопрос и ответ в базу."""
        question_entry = {
            "id": hashlib.md5(f"{question}_{tradition_id}_{datetime.now().isoformat()}".encode()).hexdigest()[:12],
            "question": question,
            "tradition_id": tradition_id,
            "answer": answer,
            "language": language,
            "depth": depth,
            "conversation_id": conversation_id,
            "timestamp": datetime.now().isoformat(),
            "word_count": len(answer.split()),
            "topic": self._extract_topic(question),
            "keywords": self._extract_keywords(question)
        }
        
        self.questions_db["questions"].append(question_entry)
        
        # Обновляем статистику по темам
        topic = question_entry["topic"]
        if topic not in self.questions_db["topics"]:
            self.questions_db["topics"][topic] = {
                "count": 0,
                "questions": [],
                "traditions": set()
            }
        
        self.questions_db["topics"][topic]["count"] += 1
        self.questions_db["topics"][topic]["questions"].append(question_entry["id"])
        self.questions_db["topics"][topic]["traditions"].add(tradition_id)
        
        # Конвертируем set в list для JSON
        self.questions_db["topics"][topic]["traditions"] = list(
            self.questions_db["topics"][topic]["traditions"]
        )
        
        self.questions_db["last_updated"] = datetime.now().isoformat()
        self._save_questions_db()
        
        print(f"✅ Сохранен вопрос: {question[:50]}... (тема: {topic})")
    
    def _extract_topic(self, question: str) -> str:
        """Извлекает основную тему из вопроса."""
        question_lower = question.lower()
        
        topic_keywords = {
            "fear_anxiety": ["страх", "тревога", "беспокойство", "паника", "fear", "anxiety"],
            "meaning_life": ["смысл жизни", "зачем жить", "цель жизни", "предназначение", "meaning", "purpose"],
            "relationships": ["отношения", "любовь", "семья", "дружба", "relationship", "love"],
            "money_success": ["деньги", "успех", "богатство", "карьера", "money", "success"],
            "death_loss": ["смерть", "потеря", "горе", "утрата", "death", "loss"],
            "anger": ["гнев", "злость", "ярость", "раздражение", "anger", "rage"],
            "meditation": ["медитация", "практика", "упражнение", "meditation", "practice"],
            "ethics": ["этика", "мораль", "добро", "зло", "ethics", "morality"],
            "happiness": ["счастье", "радость", "удовольствие", "happiness", "joy"],
            "health": ["здоровье", "тело", "болезнь", "health", "body"]
        }
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in question_lower for keyword in keywords):
                return topic
        
        return "general_questions"
    
    def _extract_keywords(self, question: str) -> List[str]:
        """Извлекает ключевые слова из вопроса."""
        stop_words = {"как", "что", "почему", "где", "когда", "кто", "зачем", "или", "и", "в", "на", "с",
                     "how", "what", "why", "where", "when", "who"}
        words = question.lower().split()
        keywords = [w for w in words if w not in stop_words and len(w) > 3]
        return keywords[:5]
    
    def _save_questions_db(self):
        """Сохраняет базу вопросов на диск."""
        with open(self.questions_db_path, 'w', encoding='utf-8') as f:
            json.dump(self.questions_db, f, ensure_ascii=False, indent=2)
    
    def get_popular_topics(self, min_questions: int = 3) -> List[Dict]:
        """Получает популярные темы (с минимум N вопросами)."""
        popular = []
        
        for topic, data in self.questions_db["topics"].items():
            if data["count"] >= min_questions:
                sample_questions = []
                for q_id in data["questions"][:3]:
                    for q in self.questions_db["questions"]:
                        if q["id"] == q_id:
                            sample_questions.append(q["question"])
                            break
                
                popular.append({
                    "topic": topic,
                    "question_count": data["count"],
                    "traditions": data["traditions"],
                    "sample_questions": sample_questions,
                    "avg_word_count": sum(
                        q["word_count"] for q in self.questions_db["questions"]
                        if q["id"] in data["questions"]
                    ) / len(data["questions"])
                })
        
        popular.sort(key=lambda x: x["question_count"], reverse=True)
        return popular
    
    async def generate_article_from_topic(self, topic_data: Dict, 
                                         language: str = "ru",
                                         llm_manager=None) -> Optional[str]:
        """Генерирует SEO-статью из популярной темы."""
        if not llm_manager:
            print("⚠️ LLM manager не предоставлен")
            return None
        
        topic = topic_data["topic"]
        traditions = topic_data["traditions"]
        
        print(f"\n📝 Генерация статьи по теме: {topic}")
        
        # Генерируем контент через LLM
        article_content = await self._generate_article_content(
            topic, topic_data["sample_questions"], traditions, language, llm_manager
        )
        
        # Создаем HTML файл
        article_path = self._create_article_html(
            topic, article_content, topic_data, language
        )
        
        # Обновляем sitemap
        self._update_sitemap(article_path, language)
        
        print(f"✅ Статья создана: {article_path}")
        return str(article_path)
    
    async def _generate_article_content(self, topic: str, 
                                       sample_questions: List[str],
                                       traditions: List[str],
                                       language: str,
                                       llm_manager) -> str:
        """Генерирует полный контент статьи через LLM."""
        
        if language == "ru":
            prompt = f"""Напиши подробную SEO-статью (минимум 2000 слов) на русском языке о теме "{topic}".

Вопросы пользователей по этой теме:
{chr(10).join(f"- {q}" for q in sample_questions)}

Традиции для сравнения: {', '.join(traditions)}

Структура статьи:
1. Введение (почему эта тема важна сегодня)
2. Исторический контекст и происхождение
3. Подход каждой традиции (подробно о 3-4 традициях)
4. Сравнительный анализ (что общего, чем отличаются)
5. Практические рекомендации для современной жизни
6. Реальные примеры и кейсы
7. FAQ (5-7 частых вопросов с ответами)
8. Заключение и призыв к действию

Требования:
- Пиши увлекательно и доступно
- Используй конкретные примеры и цитаты
- Добавь практические упражнения
- Включи реальные истории
- Оптимизируй для поисковых систем
- Используй подзаголовки H2 и H3
- Добавь списки и выделения

Начни статью:"""
        else:
            prompt = f"""Write a comprehensive SEO article (minimum 2000 words) in {language} about "{topic}".

User questions on this topic:
{chr(10).join(f"- {q}" for q in sample_questions)}

Traditions to compare: {', '.join(traditions)}

Article structure:
1. Introduction (why this topic matters today)
2. Historical context and origins
3. Approach of each tradition (detailed coverage of 3-4 traditions)
4. Comparative analysis (similarities and differences)
5. Practical recommendations for modern life
6. Real examples and case studies
7. FAQ (5-7 common questions with answers)
8. Conclusion and call to action

Requirements:
- Write engagingly and accessibly
- Use concrete examples and quotes
- Add practical exercises
- Include real stories
- Optimize for search engines
- Use H2 and H3 subheadings
- Add lists and highlights

Start the article:"""
        
        try:
            result = await llm_manager.generate_with_fallback(
                prompt=prompt,
                system_prompt=f"You are an expert writer specializing in philosophy, religion, and SEO content creation. Write in {language}.",
                temperature=0.6,
                max_tokens=3000
            )
            return result['response']
        except Exception as e:
            print(f"⚠️ Ошибка генерации контента: {e}")
            return f"[Article content generation failed: {e}]"
    
    def _create_article_html(self, topic: str, content: str,
                            topic_data: Dict, language: str) -> Path:
        """Создает HTML файл статьи."""
        
        slug = topic.replace('_', '-').lower()
        filename = f"{slug}-guide.html"
        
        lang_dir = self.articles_dir / language
        lang_dir.mkdir(parents=True, exist_ok=True)
        article_path = lang_dir / filename
        
        # Мета-данные
        titles = {
            "ru": {
                "fear_anxiety": "Как преодолеть страх и тревогу: мудрость мировых традиций",
                "meaning_life": "В поисках смысла жизни: философские и духовные ответы",
                "relationships": "Искусство отношений: учение 8 традиций о любви",
                "general_questions": "Мудрость веков: ответы на важные жизненные вопросы"
            },
            "en": {
                "fear_anxiety": "How to Overcome Fear and Anxiety: Wisdom from World Traditions",
                "meaning_life": "Searching for Meaning: Philosophical and Spiritual Answers",
                "relationships": "The Art of Relationships: Teachings from 8 Traditions",
                "general_questions": "Timeless Wisdom: Answers to Life's Important Questions"
            }
        }
        
        title = titles.get(language, {}).get(topic, 
                   f"Мудрость о {topic.replace('_', ' ')}" if language == "ru"
                   else f"Wisdom about {topic.replace('_', ' ')}")
        
        description = f"Полное руководство по теме '{topic}' с ответами от {len(topic_data['traditions'])} традиций."
        
        # Генерируем HTML
        html_template = f"""<!DOCTYPE html>
<html lang="{language}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Answers Platform</title>
    <meta name="description" content="{description}">
    <meta name="keywords" content="{topic}, философия, религия, мудрость">
    
    <!-- Open Graph -->
    <meta property="og:type" content="article">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:url" content="https://answers-platform.com/articles/{language}/{filename}">
    
    <!-- Schema.org -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": "{title}",
        "description": "{description}",
        "datePublished": "{datetime.now().isoformat()}",
        "author": {{
            "@type": "Organization",
            "name": "Answers Platform"
        }}
    }}
    </script>
    
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.8; max-width: 900px; margin: 0 auto; padding: 40px 20px; color: #333; }}
        h1 {{ color: #667eea; font-size: 2.5em; margin-bottom: 20px; }}
        h2 {{ color: #764ba2; font-size: 2em; margin: 40px 0 20px; border-bottom: 2px solid #f0f0f0; padding-bottom: 10px; }}
        h3 {{ color: #667eea; font-size: 1.5em; margin: 30px 0 15px; }}
        p {{ margin-bottom: 20px; text-align: justify; }}
        ul, ol {{ margin: 20px 0; padding-left: 30px; }}
        li {{ margin-bottom: 10px; }}
        blockquote {{ border-left: 4px solid #667eea; padding: 20px 30px; margin: 30px 0; background: #f8f9ff; font-style: italic; }}
        .faq-item {{ background: #f8f9fa; padding: 20px; margin: 15px 0; border-radius: 8px; }}
        .faq-item h4 {{ color: #764ba2; margin-bottom: 10px; }}
        footer {{ margin-top: 60px; padding-top: 30px; border-top: 2px solid #e0e0e0; text-align: center; color: #666; }}
    </style>
</head>
<body>
    <article>
        <h1>{title}</h1>
        
        {content}
        
    </article>
    
    <footer>
        <p>&copy; 2024 Answers Platform. Сгенерировано автоматически на основе {topic_data['question_count']} пользовательских вопросов.</p>
        <p><a href="/">← Вернуться на главную</a></p>
    </footer>
</body>
</html>"""
        
        with open(article_path, 'w', encoding='utf-8') as f:
            f.write(html_template)
        
        return article_path
    
    def _update_sitemap(self, article_path: Path, language: str):
        """Обновляет sitemap.xml с новой статьей."""
        sitemap_path = Path("public/sitemap.xml")
        
        if not sitemap_path.exists():
            print("⚠️ Sitemap не найден, пропускаем обновление")
            return
        
        # Читаем текущий sitemap
        with open(sitemap_path, 'r', encoding='utf-8') as f:
            sitemap_content = f.read()
        
        # Добавляем новую запись перед закрывающим тегом
        new_entry = f"""
    <url>
        <loc>https://answers-platform.com/articles/{language}/{article_path.name}</loc>
        <lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
"""
        
        sitemap_content = sitemap_content.replace('</urlset>', new_entry + '</urlset>')
        
        with open(sitemap_path, 'w', encoding='utf-8') as f:
            f.write(sitemap_content)
        
        print(f"✅ Sitemap обновлен")


# Глобальный экземпляр для использования в других модулях
article_generator = ArticleGenerator()
