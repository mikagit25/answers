# 📘 Answers Platform

> AI-powered Q&A platform providing answers to life, ethical, and spiritual questions across 8 philosophical and religious traditions, with mandatory source citations.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Next.js](https://img.shields.io/badge/Next.js-14-black.svg)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)](https://fastapi.tiangolo.com/)

---

## 🌟 Features

- **8 Traditions Supported**: Stoicism, Christianity, Islam, Buddhism, Judaism, Hinduism, Taoism, Secular Humanism
- **Authentic Sources**: Every answer includes 2-4 verified quotes with references
- **Multi-Provider LLM System**: Automatic fallback between Groq, OpenRouter, Ollama (local), HuggingFace
- **Zero-Cost Operation**: Works completely free with local Ollama or free API tiers
- **Cross-Tradition Comparison**: See how different traditions approach the same question
- **Progressive Web App**: Install on your device, works offline
- **Mobile-First Design**: Fully responsive from 320px to 1920px
- **Privacy-Focused**: No religious preference tracking without consent
- **API-First Architecture**: Easy to extend to mobile apps, Telegram bots, etc.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- (Optional) Ollama for local LLM: https://ollama.ai/

### Installation

**Option 1: Automated Setup (Recommended)**
```bash
./setup.sh
```

**Option 2: Manual Setup**

See [QUICKSTART.md](QUICKSTART.md) for detailed instructions.

### Configuration

**Minimum setup (using only free providers):**

1. **Get Groq API key** (free, 5 min): https://console.groq.com/
2. **Copy .env.example to .env** and add your key:
   ```bash
   cp .env.example backend/.env
   # Edit backend/.env and add: GROQ_API_KEY=your_key_here
   ```

**Or use completely free local setup:**
```bash
# Install Ollama: https://ollama.ai/
ollama pull llama3.2
ollama serve
# No API keys needed!
```

See [LLM_PROVIDERS_GUIDE.md](LLM_PROVIDERS_GUIDE.md) for complete setup instructions.

### Running the Application

```bash
# Terminal 1 - Start databases
docker-compose up -d

# Terminal 2 - Import knowledge base
cd backend && python ingest.py

# Terminal 3 - Run backend
cd backend && uvicorn main:app --reload

# Terminal 4 - Run frontend
cd frontend && npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## 🤖 Multi-Provider LLM System

The platform uses an intelligent fallback system that automatically switches between multiple LLM providers:

### Provider Priority (Configurable)
1. **Groq** - Fastest, free tier (30 req/min, 200 req/day)
2. **OpenRouter** - Free models available
3. **Ollama** - Local, completely free, no limits ⭐
4. **HuggingFace** - Free tier fallback

### Benefits
- ✅ **Never hits rate limits** - automatically switches to next provider
- ✅ **Zero cost option** - use local Ollama for unlimited free usage
- ✅ **Maximum reliability** - 4 different providers as backup
- ✅ **Automatic failover** - no manual intervention needed

### Quick Test
```bash
cd backend && python test_llm_providers.py
```

See [LLM_PROVIDERS_GUIDE.md](LLM_PROVIDERS_GUIDE.md) for detailed setup.

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [LLM_PROVIDERS_GUIDE.md](LLM_PROVIDERS_GUIDE.md) | **NEW!** Complete guide to setting up free LLM providers |
| [QUICKSTART.md](QUICKSTART.md) | Detailed setup and usage guide |
| [DEVELOPMENT_CHECKLIST.md](DEVELOPMENT_CHECKLIST.md) | Task tracking and remaining work |
| [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | Complete overview of what's been built |
| [TZ_answers.md](TZ_answers.md) | Original technical specification (Russian) |

---

## 🏗️ Architecture

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   Frontend   │◄───────►│   Backend     │◄───────►│   Database   │
│  Next.js 14  │  HTTP   │  FastAPI      │  SQL    │ PostgreSQL  │
│  + PWA      │  JSON   │  + RAG        │         │ + pgvector  │
└─────────────┘         └──────────────┘         └─────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  LLM Provider Mgr   │
                    │  Auto-Fallback:     │
                    │  Groq → OpenRouter  │
                    │  → Ollama → HF      │
                    └─────────────────────┘
```

### Tech Stack

**Backend:**
- FastAPI, SQLAlchemy, pgvector, LangChain, sentence-transformers
- **NEW**: Multi-provider LLM manager with automatic fallback

**Frontend:**
- Next.js 14, React 18, TypeScript, TailwindCSS, next-pwa

**Infrastructure:**
- PostgreSQL 15, Redis 7, Docker Compose

**LLM Providers:**
- Groq, OpenRouter, Ollama (local), HuggingFace

---

## 📊 Project Status

**Current Completion: ~70% MVP**

✅ **Completed:**
- Full project structure
- Database models and migrations
- RAG pipeline with 8 tradition prompts
- Backend API endpoints (/ask, /compare, /health)
- Frontend components (TraditionSelector, QuestionInput, AnswerCard)
- PWA support (manifest, install prompt, service worker)
- Sample knowledge base (Stoicism)

⚠️ **Remaining:**
- Add knowledge base data for 7 more traditions
- Implement Redis caching
- Create compare page UI
- Add user query history
- Comprehensive testing
- Production deployment configs

See [DEVELOPMENT_CHECKLIST.md](DEVELOPMENT_CHECKLIST.md) for full details.

---

## 🧪 Testing

```bash
# Backend tests
cd backend && pytest tests/ -v

# Frontend tests (coming soon)
cd frontend && npm test

# Verify setup
cd backend && python check_setup.py
```

---

## 📝 API Documentation

Once running, visit:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Example Request

```bash
curl -X POST http://localhost:8000/api/v1/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Как преодолеть страх перед будущим?",
    "tradition_id": "stoicism",
    "depth": "basic"
  }'
```

### Example Response

```json
{
  "answer": "В стоицизме страх перед будущим преодолевается через...",
  "sources": [
    {
      "text": "Мы страдаем чаще в воображении, чем в действительности.",
      "reference": "Сенека, Нравственные письма к Луцилию, Письмо 13, §4",
      "translation": "пер. С. Ошерова",
      "commentary": "О природе беспокойства о будущем"
    }
  ],
  "tradition_id": "stoicism",
  "share_url": "/answer/stoicism-kak-preodolet-strakh-a1b2c3",
  "status": "success"
}
```

---

## 🤝 Contributing

Contributions are welcome! Please read our contributing guidelines (coming soon).

**To add a new tradition:**
1. Create `knowledge_base/traditions/{id}.json`
2. Follow the Stoicism example format
3. Include 10-20 quality sources
4. Run `cd backend && python ingest.py`

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details

---

## 🙏 Acknowledgments

- **Qwen API** by Alibaba Cloud for AI capabilities
- **pgvector** for efficient vector similarity search
- **LangChain** for RAG orchestration
- All translators and scholars whose work makes authentic citations possible

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/your-repo/answers/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-repo/answers/discussions)

---

**Built with ❤️ for seekers of wisdom across all traditions**
