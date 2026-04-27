# 🚀 БЫСТРОЕ ПОДКЛЮЧЕНИЕ QWEN - 5 МИНУТ

## ✅ КРАТКИЙ ОТВЕТ

**ДА!** Вы можете использовать одну модель Qwen на нескольких проектах одновременно через HTTP API.

---

## ⚡ БЫСТРЫЙ СТАРТ (3 шага)

### Шаг 1: Запустите Qwen сервер

**Самый простой способ - Ollama:**
```bash
# На сервере с GPU (или даже CPU для небольших моделей):
ollama serve
ollama pull qwen2.5:7b
```

Сервер будет доступен на `http://your-server-ip:11434`

---

### Шаг 2: Настройте Answers Platform

Добавьте в файл `.env`:

```bash
# Подключение к удаленному Qwen серверу
QWEN_API_BASE_URL=http://192.168.1.100:11434/v1
QWEN_MODEL=qwen2.5:7b

# Приоритет провайдеров (Qwen первым)
LLM_PROVIDER_PRIORITY=qwen,groq,openrouter,ollama,huggingface
```

**Замените `192.168.1.100` на IP вашего сервера с Qwen.**

---

### Шаг 3: Перезапустите backend

```bash
cd backend
uvicorn main:app --reload
```

**Готово!** 🎉 Теперь проект использует Qwen.

---

## 🌐 ПОДКЛЮЧЕНИЕ ВТОРОГО ПРОЕКТА

На втором проекте сделайте то же самое:

```bash
# .env второго проекта
QWEN_API_BASE_URL=http://192.168.1.100:11434/v1  # Тот же сервер!
QWEN_MODEL=qwen2.5:7b
```

**Оба проекта теперь используют один Qwen сервер!**

---

## 📊 ЧТО МОЖЕТ ОДИН СЕРВЕР?

| Модель | GPU | Одновременных запросов | Проектов |
|--------|-----|----------------------|----------|
| Qwen 7B | RTX 3090/4090 | 5-10 (Ollama) / 50+ (vLLM) | 10-50+ |
| Qwen 14B | A100 40GB | 3-5 (Ollama) / 30+ (vLLM) | 5-30+ |
| Qwen 72B | A100 80GB | 1-2 (Ollama) / 10+ (vLLM) | 2-10+ |

**Для Answers Platform (1000 users/day):**
- Нужно ~0.06 запросов/секунду
- **Один сервер легко потянет 50+ проектов!**

---

## 🔧 ПРОДВИНУТАЯ НАСТРОЙКА (vLLM)

Для максимальной производительности:

```bash
# Установка vLLM
pip install vllm

# Запуск с OpenAI-compatible API
python -m vllm.entrypoints.openai.api_server \
    --model Qwen/Qwen2.5-7B-Instruct \
    --tensor-parallel-size 2 \
    --port 8000 \
    --host 0.0.0.0
```

В `.env`:
```bash
QWEN_API_BASE_URL=http://your-server:8000/v1
```

**Преимущества vLLM:**
- ⚡ В 5-10 раз быстрее Ollama
- 🔄 Continuous batching (больше concurrent requests)
- 📈 Better GPU utilization

---

## 🔒 БЕЗОПАСНОСТЬ (если сервер в интернете)

**1. Добавьте API key:**

На сервере (nginx конфигурация):
```nginx
location /v1/ {
    auth_basic "Restricted";
    auth_basic_user_file /etc/nginx/.htpasswd;
    proxy_pass http://localhost:8000;
}
```

В `.env` каждого проекта:
```bash
QWEN_API_KEY=your-secret-password
```

**2. Используйте HTTPS:**
```bash
certbot --nginx -d qwen.yourdomain.com
```

---

## 🎯 ПРОВЕРКА РАБОТЫ

**Тест через curl:**
```bash
curl http://your-server:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen2.5:7b",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

**Тест из Python:**
```python
import httpx

async def test_qwen():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://your-server:11434/v1/chat/completions",
            json={
                "model": "qwen2.5:7b",
                "messages": [{"role": "user", "content": "What is AI?"}]
            }
        )
        print(response.json()["choices"][0]["message"]["content"])

import asyncio
asyncio.run(test_qwen())
```

---

## 💰 СТОИМОСТЬ

**Self-hosted Qwen:**
- Cloud GPU server: $200-500/месяц
- Или свое железо: $2000-3000 один раз
- Electricity: $20-50/месяц

**На 5 проектов:**
- $40-100/месяц каждый
- **Экономия vs GPT-4: 95%+** ($300 → $50)

---

## ❓ ЧАСТЫЕ ВОПРОСЫ

**Q: Что если сервер упадет?**  
A: Система автоматически переключится на backup провайдер (Groq, OpenRouter). Никакого downtime!

**Q: Можно ли без интернета?**  
A: Да! Self-hosted Qwen работает полностью offline.

**Q: Сколько проектов потянет один сервер?**  
A: Для typical usage (1000 users/day per project): 50+ проектов легко.

**Q: Нужен ли мощный GPU?**  
A: Для Qwen 7B хватит RTX 3090 (24GB VRAM). Для production лучше A100.

**Q: Можно ли использовать бесплатно?**  
A: Да! Qwen open-source. Платите только за hardware/electricity.

---

## 📚 ПОДРОБНАЯ ДОКУМЕНТАЦИЯ

Полная документация: [QWEN_INTEGRATION_GUIDE.md](QWEN_INTEGRATION_GUIDE.md)

---

**Готово к использованию!** ✅  
Qwen provider уже добавлен в код. Просто настройте `.env` и запустите сервер.
