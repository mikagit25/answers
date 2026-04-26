"""
Минимальный тестовый сервер с поддержкой мультиязычности, диалогового контекста и автоматической генерации статей.
"""
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import asyncio
import sys
from pathlib import Path
import time

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from core.llm_manager import llm_manager
from core.i18n import SUPPORTED_LANGUAGES, get_translation, detect_language_from_headers
from core.article_generator import article_generator

app = FastAPI(title="Answers API - Multilingual with Auto-Articles", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Хранилище диалогов (in-memory для демо, в продакшене использовать Redis/PostgreSQL)
conversation_store = {}


class QuestionRequest(BaseModel):
    question: str
    tradition_id: str = "stoicism"
    language: Optional[str] = None
    conversation_id: Optional[str] = None  # ID текущего диалога
    depth: Optional[str] = "basic"  # basic/detailed/comprehensive


class CompareRequest(BaseModel):
    question: str
    exclude: Optional[str] = None
    language: Optional[str] = None


class FollowUpRequest(BaseModel):
    question: str
    tradition_id: str
    conversation_id: str
    language: Optional[str] = None
    context_window: Optional[int] = 3  # Сколько предыдущих сообщений учитывать


@app.get("/health")
def health_check(request: Request):
    """Health check with language detection"""
    lang = detect_language_from_headers(request.headers)
    return {
        "status": "ok",
        "providers": llm_manager.get_available_providers(),
        "detected_language": lang,
        "message": get_translation(lang, "app_title"),
        "active_conversations": len(conversation_store)
    }


@app.get("/api/v1/languages")
def get_languages():
    """Get list of supported languages"""
    languages = []
    for code, info in SUPPORTED_LANGUAGES.items():
        languages.append({
            "code": code,
            "name": info["name"],
            "native_name": info["native_name"],
            "flag": info["flag"],
            "direction": info["direction"]
        })
    return {"languages": languages}


@app.post("/api/v1/conversations/new")
async def create_conversation():
    """Create a new conversation session"""
    import uuid
    conversation_id = str(uuid.uuid4())
    conversation_store[conversation_id] = {
        "messages": [],
        "created_at": time.time(),
        "last_updated": time.time()
    }
    
    # Очистка старых диалогов (старше 24 часов)
    cleanup_old_conversations()
    
    return {
        "conversation_id": conversation_id,
        "status": "created"
    }


@app.get("/api/v1/conversations/{conversation_id}")
def get_conversation(conversation_id: str):
    """Get conversation history"""
    if conversation_id not in conversation_store:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    conv = conversation_store[conversation_id]
    return {
        "conversation_id": conversation_id,
        "messages": conv["messages"],
        "message_count": len(conv["messages"])
    }


@app.post("/api/v1/ask")
async def ask_question(request: QuestionRequest, http_request: Request):
    """
    Question answering with language support and conversation context.
    """
    try:
        # Detect language
        lang = request.language or detect_language_from_headers(http_request.headers)
        
        # Determine token limits based on depth
        if request.depth == "comprehensive":
            max_tokens = 800
            temperature = 0.5
        elif request.depth == "detailed":
            max_tokens = 500
            temperature = 0.4
        else:  # basic
            max_tokens = 300
            temperature = 0.3
        
        print(f"\n📨 Question: {request.question}")
        print(f"🎯 Tradition: {request.tradition_id}")
        print(f"🌍 Language: {lang}")
        print(f"📊 Depth: {request.depth} (max_tokens: {max_tokens})")
        
        # Get tradition name in selected language
        tradition_key = f"tradition_{request.tradition_id}"
        tradition_name = get_translation(lang, tradition_key, request.tradition_id)
        
        # Build context from conversation history if exists
        context_prompt = ""
        if request.conversation_id and request.conversation_id in conversation_store:
            conv = conversation_store[request.conversation_id]
            recent_messages = conv["messages"][-5:]  # Last 5 messages
            
            if recent_messages:
                context_prompt = "\n\nPrevious conversation context:\n"
                for msg in recent_messages:
                    role = "User" if msg["role"] == "user" else "Assistant"
                    context_prompt += f"{role}: {msg['content'][:200]}...\n"
                context_prompt += "\nBased on this context, provide a coherent follow-up answer.\n"
        
        # Create comprehensive prompt
        if lang == "ru":
            system_prompt = f"""Ты эксперт по {tradition_name} с глубокими знаниями.
            
{context_prompt}

Ответь на вопрос максимально полно и развернуто, основываясь на философии {tradition_name}.
Структурируй ответ:
1. Краткое введение в подход традиции
2. Основной ответ с объяснением принципов
3. Практические рекомендации или примеры
4. Заключение

Отвечай на русском языке. Будь подробным но ясным."""
            
            prompt = f"Вопрос: {request.question}"
            
        elif lang == "ar":
            system_prompt = f"""أنت خبير في {tradition_name} مع معرفة عميقة.
            
{context_prompt}

أجب على السؤال بشكل شامل ومفصل بناءً على فلسفة {tradition_name}.
نظم إجابتك:
1. مقدمة موجزة عن نهج التقليد
2. الإجابة الرئيسية مع شرح المبادئ
3. توصيات عملية أو أمثلة
4. خاتمة

أجب باللغة العربية. كن مفصلاً ولكن واضحاً."""
            
            prompt = f"السؤال: {request.question}"
            
        else:
            system_prompt = f"""You are an expert in {tradition_name} with deep knowledge.
            
{context_prompt}

Answer the question comprehensively and in detail based on {tradition_name} philosophy.
Structure your response:
1. Brief introduction to the tradition's approach
2. Main answer with explanation of principles
3. Practical recommendations or examples
4. Conclusion

Answer in the same language as the question. Be detailed but clear."""
            
            prompt = f"Question: {request.question}"
        
        # Use LLM manager with increased tokens
        result = await llm_manager.generate_with_fallback(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        
        print(f"✅ Answer generated using: {result['provider']} ({len(result['response'])} chars)")
        
        # Сохраняем вопрос в базу для будущей генерации статей
        article_generator.save_question(
            question=request.question,
            tradition_id=request.tradition_id,
            answer=result["response"],
            language=lang,
            depth=request.depth,
            conversation_id=request.conversation_id
        )
        
        # Проверяем, нужно ли сгенерировать новую статью
        popular_topics = article_generator.get_popular_topics(min_questions=3)
        if popular_topics:
            print(f"📊 Найдено {len(popular_topics)} популярных тем для генерации статей")
            # Можно добавить фоновую задачу для генерации
        
        # Save to conversation history if conversation_id provided
        if request.conversation_id and request.conversation_id in conversation_store:
            conv = conversation_store[request.conversation_id]
            conv["messages"].append({
                "role": "user",
                "content": request.question,
                "timestamp": time.time()
            })
            conv["messages"].append({
                "role": "assistant",
                "content": result["response"],
                "timestamp": time.time(),
                "metadata": {
                    "tradition": request.tradition_id,
                    "depth": request.depth,
                    "tokens_used": max_tokens
                }
            })
            conv["last_updated"] = time.time()
        
        return {
            "answer": result["response"],
            "tradition_id": request.tradition_id,
            "language": lang,
            "depth": request.depth,
            "conversation_id": request.conversation_id,
            "metadata": {
                "provider": result["provider"],
                "model": result["model"],
                "fallback_used": result["fallback_used"],
                "tokens_max": max_tokens,
                "temperature": temperature,
                "has_context": bool(context_prompt)
            },
            "sources": [],
            "status": "success"
        }
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/followup")
async def follow_up_question(request: FollowUpRequest, http_request: Request):
    """
    Ask a follow-up question within an existing conversation.
    Maintains context from previous messages.
    """
    try:
        if request.conversation_id not in conversation_store:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        lang = request.language or detect_language_from_headers(http_request.headers)
        conv = conversation_store[request.conversation_id]
        
        # Get recent context
        context_window = min(request.context_window, len(conv["messages"]))
        recent_messages = conv["messages"][-context_window:] if context_window > 0 else []
        
        print(f"\n🔄 Follow-up question in conversation {request.conversation_id[:8]}...")
        print(f"📊 Context messages: {len(recent_messages)}")
        
        # Build context-aware prompt
        context_text = ""
        if recent_messages:
            context_text = "\n\nConversation history:\n"
            for i, msg in enumerate(recent_messages):
                role = "User" if msg["role"] == "user" else "Assistant"
                preview = msg["content"][:300]
                context_text += f"[Message {i+1}] {role}: {preview}\n"
        
        tradition_key = f"tradition_{request.tradition_id}"
        tradition_name = get_translation(lang, tradition_key, request.tradition_id)
        
        if lang == "ru":
            system_prompt = f"""Ты эксперт по {tradition_name}. Ты ведешь диалог с пользователем.

{context_text}

Пользователь задал уточняющий вопрос. Ответь на него, учитывая предыдущий контекст беседы.
Если вопрос связан с предыдущими ответами, сделай плавный переход.
Будь последовательным в своих объяснениях.

Отвечай на русском языке подробно."""
        else:
            system_prompt = f"""You are an expert in {tradition_name}. You are having a conversation with a user.

{context_text}

The user asked a follow-up question. Answer it considering the previous conversation context.
If the question relates to previous answers, make a smooth transition.
Be consistent in your explanations.

Answer in the same language as the question, in detail."""
        
        prompt = f"Follow-up question: {request.question}"
        
        result = await llm_manager.generate_with_fallback(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.4,
            max_tokens=600,
        )
        
        print(f"✅ Follow-up answer generated ({len(result['response'])} chars)")
        
        # Save to conversation
        conv["messages"].append({
            "role": "user",
            "content": request.question,
            "timestamp": time.time(),
            "is_followup": True
        })
        conv["messages"].append({
            "role": "assistant",
            "content": result["response"],
            "timestamp": time.time(),
            "is_followup": True
        })
        conv["last_updated"] = time.time()
        
        return {
            "answer": result["response"],
            "conversation_id": request.conversation_id,
            "language": lang,
            "context_messages": len(recent_messages),
            "metadata": {
                "provider": result["provider"],
                "model": result["model"],
                "is_contextual": True
            },
            "status": "success"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error in follow-up: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/compare")
async def compare_traditions(request: CompareRequest, http_request: Request):
    """
    Compare traditions with language support.
    """
    try:
        lang = request.language or detect_language_from_headers(http_request.headers)
        
        print(f"\n🔄 Comparing traditions for: {request.question}")
        print(f"🌍 Language: {lang}")
        
        all_traditions = [
            {"id": "stoicism", "name": get_translation(lang, "tradition_stoicism")},
            {"id": "christianity", "name": get_translation(lang, "tradition_christianity")},
            {"id": "islam", "name": get_translation(lang, "tradition_islam")},
            {"id": "buddhism", "name": get_translation(lang, "tradition_buddhism")},
            {"id": "judaism", "name": get_translation(lang, "tradition_judaism")},
            {"id": "hinduism", "name": get_translation(lang, "tradition_hinduism")},
            {"id": "taoism", "name": get_translation(lang, "tradition_taoism")},
            {"id": "humanism", "name": get_translation(lang, "tradition_humanism")}
        ]
        
        traditions_to_compare = [
            t for t in all_traditions 
            if t["id"] != request.exclude
        ][:3]
        
        print(f"📊 Comparing with: {[t['name'] for t in traditions_to_compare]}")
        
        comparisons = []
        
        for tradition in traditions_to_compare:
            try:
                if lang == "ru":
                    prompt = f"""Ты эксперт по {tradition['name']}.
Подробно объясни (100-150 слов), как {tradition['name']} отвечает на этот вопрос:

Вопрос: {request.question}

Отвечай на русском языке. Дай развернутый ответ с примерами."""
                elif lang == "ar":
                    prompt = f"""أنت خبير في {tradition['name']}.
اشرح بالتفصيل (100-150 كلمة) كيف تجيب {tradition['name']} على هذا السؤال:

السؤال: {request.question}

أجب باللغة العربية. قدم إجابة مفصلة مع أمثلة."""
                else:
                    prompt = f"""You are an expert in {tradition['name']}.
Explain in detail (100-150 words) how {tradition['name']} would answer this question:

Question: {request.question}

Answer in the same language as the question. Provide a detailed response with examples."""

                result = await llm_manager.generate_with_fallback(
                    prompt=prompt,
                    system_prompt=f"You are an expert in {tradition['name']}. Provide detailed explanations.",
                    temperature=0.4,
                    max_tokens=400,
                )
                
                comparisons.append({
                    "tradition_id": tradition["id"],
                    "tradition_name": tradition["name"],
                    "summary": result["response"],
                    "source_preview": get_translation(lang, "powered_by")
                })
                
                print(f"  ✅ Got answer from {tradition['name']}")
                
            except Exception as e:
                print(f"  ⚠️ Failed: {str(e)[:50]}")
                comparisons.append({
                    "tradition_id": tradition["id"],
                    "tradition_name": tradition["name"],
                    "summary": get_translation(lang, "no_sources"),
                    "source_preview": ""
                })
        
        return {
            "comparisons": comparisons,
            "question": request.question,
            "excluded_tradition": request.exclude,
            "language": lang
        }
        
    except Exception as e:
        print(f"❌ Error in compare: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/v1/conversations/{conversation_id}")
def delete_conversation(conversation_id: str):
    """Delete a conversation"""
    if conversation_id not in conversation_store:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    del conversation_store[conversation_id]
    return {"status": "deleted", "conversation_id": conversation_id}


@app.get("/api/v1/providers/status")
def get_providers_status():
    """Get status of all LLM providers"""
    return llm_manager.get_stats()


@app.get("/api/v1/articles/popular-topics")
def get_popular_topics_endpoint(min_questions: int = 3):
    """Get popular topics for article generation based on user questions."""
    try:
        popular = article_generator.get_popular_topics(min_questions=min_questions)
        
        return {
            "popular_topics": popular,
            "total_topics": len(popular),
            "total_questions": len(article_generator.questions_db["questions"]),
            "last_updated": article_generator.questions_db["last_updated"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/articles/generate")
async def generate_article_endpoint(topic: str = None, language: str = "ru"):
    """
    Manually trigger article generation for a specific topic.
    If topic is not provided, generates for the most popular topic.
    """
    try:
        popular_topics = article_generator.get_popular_topics(min_questions=2)
        
        if not popular_topics:
            raise HTTPException(
                status_code=404, 
                detail="Not enough questions to generate articles. Need at least 2 questions per topic."
            )
        
        # Find topic or use most popular
        target_topic = None
        if topic:
            for t in popular_topics:
                if t["topic"] == topic:
                    target_topic = t
                    break
            if not target_topic:
                raise HTTPException(status_code=404, detail=f"Topic '{topic}' not found or has insufficient questions")
        else:
            target_topic = popular_topics[0]  # Most popular
        
        print(f"\n📝 Starting article generation for topic: {target_topic['topic']}")
        
        # Generate article
        article_path = await article_generator.generate_article_from_topic(
            topic_data=target_topic,
            language=language,
            llm_manager=llm_manager
        )
        
        if not article_path:
            raise HTTPException(status_code=500, detail="Failed to generate article")
        
        return {
            "status": "success",
            "article_path": article_path,
            "topic": target_topic["topic"],
            "question_count": target_topic["question_count"],
            "traditions": target_topic["traditions"],
            "language": language
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Article generation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/articles/generate-all")
async def generate_all_articles(language: str = "ru"):
    """Generate articles for all popular topics."""
    try:
        popular_topics = article_generator.get_popular_topics(min_questions=2)
        
        if not popular_topics:
            raise HTTPException(
                status_code=404,
                detail="No popular topics found. Need more user questions."
            )
        
        results = []
        for topic_data in popular_topics:
            try:
                print(f"\n📝 Generating article for: {topic_data['topic']}")
                article_path = await article_generator.generate_article_from_topic(
                    topic_data=topic_data,
                    language=language,
                    llm_manager=llm_manager
                )
                
                if article_path:
                    results.append({
                        "topic": topic_data["topic"],
                        "path": article_path,
                        "status": "success"
                    })
                else:
                    results.append({
                        "topic": topic_data["topic"],
                        "status": "failed"
                    })
            except Exception as e:
                print(f"⚠️ Failed to generate article for {topic_data['topic']}: {e}")
                results.append({
                    "topic": topic_data["topic"],
                    "status": "error",
                    "error": str(e)
                })
        
        return {
            "status": "completed",
            "total_topics": len(popular_topics),
            "successful": sum(1 for r in results if r["status"] == "success"),
            "failed": sum(1 for r in results if r["status"] in ["failed", "error"]),
            "results": results
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Batch generation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


def cleanup_old_conversations():
    """Remove conversations older than 24 hours"""
    current_time = time.time()
    expired_ids = [
        conv_id for conv_id, conv in conversation_store.items()
        if current_time - conv["created_at"] > 86400  # 24 hours
    ]
    
    for conv_id in expired_ids:
        del conversation_store[conv_id]
    
    if expired_ids:
        print(f"🧹 Cleaned up {len(expired_ids)} expired conversations")


if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*70)
    print("🚀 Answers API - Multilingual Server with Conversation Context")
    print("="*70)
    print(f"📍 API Docs: http://localhost:8000/docs")
    print(f"🌍 Supported Languages: {len(SUPPORTED_LANGUAGES)}")
    
    lang_list = [f"{info['flag']} {info['name']}" for info in SUPPORTED_LANGUAGES.values()]
    print(f"   Languages: {', '.join(lang_list)}")
    
    print(f"🤖 Available providers: {llm_manager.get_available_providers()}")
    print(f"💬 Conversation store: In-memory (auto-cleanup after 24h)")
    print(f"\n📊 Features:")
    print(f"   ✓ Multi-depth answers (basic/detailed/comprehensive)")
    print(f"   ✓ Conversation context & follow-up questions")
    print(f"   ✓ Increased token limits (300-800 tokens)")
    print(f"   ✓ Structured responses with sections")
    print("="*70 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
