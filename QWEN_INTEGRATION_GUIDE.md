## 🔧 КАК ПОДКЛЮЧИТЬ QWEN К ANSWERS PLATFORM

Я добавил Qwen как новый провайдер в систему. Теперь нужно настроить подключение.

### Шаг 1: Настройка сервера Qwen

**Вариант A: vLLM (Рекомендуется для production)**

```bash
# На сервере с GPU:
pip install vllm

# Запуск Qwen с OpenAI-compatible API
python -m vllm.entrypoints.openai.api_server \
    --model Qwen/Qwen2.5-7B-Instruct \
    --tensor-parallel-size 2 \
    --port 8000 \
    --host 0.0.0.0
```

**Вариант B: Ollama (Простой способ)**

```bash
# На любом сервере:
ollama serve

# Pull Qwen модель
ollama pull qwen2.5:7b

# API будет доступен на порту 11434
```

**Вариант C: Text Generation Inference (TGI)**

```bash
docker run --gpus all \
    -p 8000:80 \
    ghcr.io/huggingface/text-generation-inference:latest \
    --model-id Qwen/Qwen2.5-7B-Instruct \
    --num-shard 2
```

---

### Шаг 2: Конфигурация Answers Platform

Добавьте в `.env` файл вашего проекта:

```bash
# Qwen API Configuration
QWEN_API_BASE_URL=http://your-qwen-server-ip:8000/v1
QWEN_API_KEY=  # Оставьте пустым если нет аутентификации
QWEN_MODEL=qwen2.5-7b-instruct

# Обновите приоритет провайдеров (опционально)
LLM_PROVIDER_PRIORITY=groq,openrouter,qwen,ollama,huggingface
```

**Примеры URL:**
```bash
# Локальный сервер (тот же хост)
QWEN_API_BASE_URL=http://localhost:8000/v1

# Удаленный сервер в локальной сети
QWEN_API_BASE_URL=http://192.168.1.100:8000/v1

# Сервер в интернете (с HTTPS)
QWEN_API_BASE_URL=https://qwen.yourdomain.com/v1

# Ollama формат
QWEN_API_BASE_URL=http://192.168.1.100:11434/v1
QWEN_MODEL=qwen2.5:7b
```

---

### Шаг 3: Тестирование подключения

```bash
cd backend
python test_llm_providers.py
```

Или через curl напрямую к Qwen серверу:

```bash
curl http://your-qwen-server:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen2.5-7b-instruct",
    "messages": [{"role": "user", "content": "Hello!"}],
    "temperature": 0.7
  }'
```

---

## 🌐 ИСПОЛЬЗОВАНИЕ QWEN НА НЕСКОЛЬКИХ ПРОЕКТАХ

### ✅ ДА! Один сервер Qwen может обслуживать множество проектов одновременно.

**Архитектура:**

```
                    ┌─────────────────┐
                    │  Qwen Server    │
                    │  (GPU Server)   │
                    │                 │
                    │  Port: 8000     │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
     ┌────────▼──────┐ ┌────▼──────┐ ┌─────▼──────┐
     │ Project 1     │ │ Project 2 │ │ Project 3  │
     │ Answers       │ │ Другой    │ │ Третий     │
     │ Platform      │ │ сайт      │ │ проект     │
     │               │ │           │ │            │
     │ .env:         │ │ .env:     │ │ .env:      │
     │ QWEN_API_     │ │ QWEN_API_ │ │ QWEN_API_  │
     │ BASE_URL=     │ │ BASE_URL= │ │ BASE_URL=  │
     │ http://server │ │ http://   │ │ http://    │
     │ :8000/v1      │ │ server    │ │ server     │
     │               │ │ :8000/v1  │ │ :8000/v1   │
     └───────────────┘ └───────────┘ └────────────┘
```

**Все проекты подключаются к одному серверу по HTTP API!**

---

## 📊 ПРОИЗВОДИТЕЛЬНОСТЬ И МАСШТАБИРОВАНИЕ

### Concurrent Requests (Одновременные запросы)

**Qwen 7B на одном GPU может обрабатывать:**
- **vLLM**: 50-100 concurrent requests (с continuous batching)
- **Ollama**: 5-10 concurrent requests
- **TGI**: 30-50 concurrent requests

**Для Answers Platform:**
- При 1,000 users/day × 5 questions/user = 5,000 requests/day
- Это ~0.06 requests/second (очень низкая нагрузка!)
- **Один сервер легко справится с 10+ проектами**

### Load Balancing (При высокой нагрузке)

Если нужно больше производительности:

```
                    ┌──────────────┐
                    │ Load Balancer│
                    │ (nginx/HAProxy)
                    └──────┬───────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
     ┌────────▼───┐ ┌─────▼────┐ ┌────▼─────┐
     │ Qwen GPU 1 │ │ Qwen GPU2│ │ Qwen GPU3│
     └────────────┘ └──────────┘ └──────────┘
```

**nginx конфигурация:**
```nginx
upstream qwen_backend {
    server qwen-server-1:8000;
    server qwen-server-2:8000;
    server qwen-server-3:8000;
}

server {
    listen 80;
    
    location /v1/ {
        proxy_pass http://qwen_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 🔒 БЕЗОПАСНОСТЬ

### Если Qwen сервер доступен из интернета:

**1. Добавьте API Key аутентификацию:**

```bash
# В .env каждого проекта:
QWEN_API_KEY=your-secret-key-here
```

**2. Настройте nginx с basic auth:**

```nginx
location /v1/ {
    auth_basic "Restricted";
    auth_basic_user_file /etc/nginx/.htpasswd;
    
    proxy_pass http://qwen_backend;
}
```

**3. Используйте HTTPS:**

```bash
# С Let's Encrypt (бесплатно):
certbot --nginx -d qwen.yourdomain.com
```

**4. Ограничьте доступ по IP (если возможно):**

```nginx
allow 192.168.1.0/24;  # Ваша локальная сеть
allow 203.0.113.5;     # IP вашего проекта
deny all;
```

---

## 💰 СТОИМОСТЬ

### Self-hosted Qwen (Один сервер для всех проектов):

**Hardware requirements:**
- GPU: NVIDIA RTX 3090/4090 (24GB VRAM) или A100 (40-80GB)
- RAM: 32-64 GB
- Storage: 100 GB SSD
- CPU: 8+ cores

**Costs:**
- Server: $200-500/месяц (cloud GPU instance)
- Или один раз $2000-3000 (собственное железо)
- Electricity: $20-50/месяц

**Per project cost:**
- Если 5 проектов используют один сервер: $40-100/месяц каждый
- Если 10 проектов: $20-50/месяц каждый
- **Гораздо дешевле чем paid APIs!**

### Сравнение с платными API:

| Provider | Cost per 1K tokens | Monthly cost (10K queries) |
|----------|-------------------|---------------------------|
| GPT-4    | $0.03             | $300+                     |
| Claude   | $0.024            | $240+                     |
| **Qwen (self-hosted)** | **$0.001** (electricity) | **$10-20** |
| **Экономия:** | **95%+** | **$220-290/месяц** |

---

## 🎯 ПРАКТИЧЕСКИЕ СЦЕНАРИИ

### Сценарий 1: Два ваших проекта

```
Project 1: answers-platform.com
Project 2: another-project.com

Оба подключены к:
QWEN_API_BASE_URL=http://shared-gpu-server:8000/v1

Преимущества:
✅ Экономия costs (один GPU вместо двух)
✅ Централизованное управление
✅ Легко обновлять модель
✅ Consistent performance
```

### Сценарий 2: Команда разработчиков

```
Developer 1: localhost project
Developer 2: localhost project  
Developer 3: staging environment
Production: live site

Все подключены к одному dev Qwen серверу:
QWEN_API_BASE_URL=http://dev-server.local:8000/v1

Преимущества:
✅ Не нужно запускать модель на каждом компе
✅ Экономия ресурсов developer machines
✅ Единая точка тестирования
```

### Сценарий 3: SaaS платформа

```
Customer 1 → Your API → Qwen Server
Customer 2 → Your API → Qwen Server
Customer 3 → Your API → Qwen Server

Вы предоставляете API клиентам,
все запросы идут через ваш Qwen сервер.

Преимущества:
✅ Полный контроль над costs
✅ Можно мониторить usage
✅ Rate limiting per customer
✅ Custom model fine-tuning
```

---

## 🛠️ МОНИТОРИНГ USAGE

### Отслеживание запросов от разных проектов:

**Добавьте custom headers в запросы:**

```python
# В llm_manager.py, QwenProvider class:
headers = {
    "Content-Type": "application/json",
    "X-Project-ID": "answers-platform",  # Уникальный ID проекта
    "X-Request-Source": os.getenv("PROJECT_NAME", "unknown"),
}

if settings.QWEN_API_KEY:
    headers["Authorization"] = f"Bearer {settings.QWEN_API_KEY}"
```

**На сервере Qwen логируйте:**
```python
# В middleware сервера:
project_id = request.headers.get("X-Project-ID")
log_usage(project_id, tokens_used, timestamp)
```

**Dashboard для мониторинга:**
- Requests per project per day
- Token usage breakdown
- Cost allocation
- Performance metrics

---

## 🚀 БЫСТРЫЙ СТАРТ

### Минимальная настройка за 5 минут:

**1. На сервере с GPU:**
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama
ollama serve &

# Pull Qwen
ollama pull qwen2.5:7b
```

**2. В Answers Platform (.env):**
```bash
QWEN_API_BASE_URL=http://your-server-ip:11434/v1
QWEN_MODEL=qwen2.5:7b
LLM_PROVIDER_PRIORITY=qwen,ollama
```

**3. Restart backend:**
```bash
cd backend
uvicorn main:app --reload
```

**4. Test:**
```bash
curl http://localhost:8000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the meaning of life?", "traditions": ["stoicism"]}'
```

**Готово!** 🎉

---

## ❓ FAQ

### Q: Может ли один Qwen сервер обслуживать 100+ проектов?
**A:** Да, при правильной архитектуре! С load balancer и несколькими GPU инстансами можно масштабировать до тысяч проектов.

### Q: Что если сервер упадет?
**A:** Система автоматически переключится на следующий провайдер (groq, openrouter, ollama). Никакого downtime для пользователей!

### Q: Нужно ли платить за использование Qwen?
**A:** Нет! Qwen полностью open-source. Вы платите только за hardware/electricity или cloud server rental.

### Q: Какая модель Qwen лучше?
**A:** 
- **Qwen2.5-7B**: Отличный баланс speed/quality для большинства задач
- **Qwen2.5-14B**: Лучше качество, требует больше VRAM
- **Qwen2.5-72B**: Best quality, нужен A100/H100 GPU

### Q: Можно ли использовать Qwen без интернета?
**A:** Да! Self-hosted Qwen работает полностью offline. Идеально для air-gapped environments.

### Q: Как защитить сервер от злоупотреблений?
**A:** 
1. API key authentication
2. Rate limiting (requests per minute per project)
3. IP whitelisting
4. Usage monitoring and alerts
5. Request quota per project

---

## 📚 ДОПОЛНИТЕЛЬНЫЕ РЕСУРСЫ

**Документация Qwen:**
- [Qwen GitHub](https://github.com/QwenLM/Qwen)
- [Qwen Documentation](https://qwen.readthedocs.io/)

**Deployment guides:**
- [vLLM Documentation](https://docs.vllm.ai/)
- [Ollama Documentation](https://ollama.ai/docs)
- [TGI Documentation](https://huggingface.co/docs/text-generation-inference)

**Performance optimization:**
- [Qwen Performance Tuning Guide](https://qwen.readthedocs.io/en/latest/deployment/vllm.html)
- [GPU Optimization Tips](https://docs.vllm.ai/en/latest/performance.html)

---

## 🎊 ЗАКЛЮЧЕНИЕ

**Да, вы можете использовать одну модель Qwen на двух (или более) сайтах одновременно!**

**Ключевые преимущества:**
✅ Экономия costs (один GPU вместо нескольких)  
✅ Централизованное управление и обновления  
✅ Автоматический fallback если сервер недоступен  
✅ Масштабируемость до сотен проектов  
✅ Полный контроль над данными и privacy  

**Рекомендуемая архитектура:**
1. Развернуть Qwen на отдельном GPU сервере
2. Настроить OpenAI-compatible API endpoint
3. Подключить все проекты через `QWEN_API_BASE_URL`
4. Добавить monitoring и rate limiting
5. Настроить backup providers для reliability

**Следующие шаги:**
1. Выберите deployment вариант (vLLM/Ollama/TGI)
2. Настройте сервер с Qwen
3. Обновите `.env` в каждом проекте
4. Протестируйте подключение
5. Monitor usage и optimize performance

---

**Дата создания:** 26 апреля 2026  
**Версия:** 1.0  
**Статус:** ✅ Qwen provider добавлен в код, готов к использованию!
