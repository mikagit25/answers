# 🆕 What's New: Multi-Provider LLM System with Automatic Fallback

## Overview

The Answers Platform now supports **multiple free LLM providers** with **automatic fallback** when rate limits are hit or providers fail. This ensures the platform can operate **completely free** while maintaining high availability.

---

## 🎯 Key Features

### 1. **Multiple Provider Support**
- ✅ **Groq** - Fastest inference, free tier (30 req/min, 200 req/day)
- ✅ **OpenRouter** - Access to many free models
- ✅ **Ollama** - Local execution, completely free, no limits
- ✅ **HuggingFace** - Free tier as last resort

### 2. **Automatic Fallback**
- System tries providers in priority order
- Automatically switches on rate limits or errors
- No manual intervention required
- Maintains service continuity

### 3. **Zero-Cost Operation**
- Use local Ollama for unlimited free usage
- Or combine free tiers of multiple providers
- No credit card required

### 4. **Intelligent Provider Management**
- Tracks success/failure rates per provider
- Disables problematic providers temporarily
- Provides statistics via API endpoint
- Manual reset capability

---

## 📦 New Files Created

### Core Implementation
1. **`backend/core/llm_manager.py`** (450+ lines)
   - Abstract base class for all providers
   - Individual provider implementations (Groq, OpenRouter, Ollama, HuggingFace)
   - `LLMProviderManager` with automatic fallback logic
   - Rate limit detection and handling
   - Usage statistics tracking

2. **`backend/api/routes/providers.py`**
   - `GET /api/v1/providers/status` - Check provider availability and stats
   - `POST /api/v1/providers/reset` - Manually reset disabled provider

### Configuration Updates
3. **`backend/core/config.py`** - Updated with multi-provider settings
4. **`.env.example`** - Comprehensive examples for all providers
5. **`backend/requirements.txt`** - Added httpx dependency

### Documentation
6. **`LLM_PROVIDERS_GUIDE.md`** (500+ lines)
   - Complete setup guide for each provider
   - Step-by-step instructions with screenshots links
   - Troubleshooting section
   - Cost comparison table
   - Best practices

7. **`backend/test_llm_providers.py`**
   - Test suite for verifying provider connectivity
   - Tests individual providers and fallback mechanism
   - Shows usage statistics

### Updates
8. **`backend/rag/pipeline.py`** - Integrated with new LLM manager
9. **`backend/main.py`** - Added providers router
10. **`README.md`** - Updated with multi-provider system info

---

## 🔧 How It Works

### Request Flow

```
User Question
     ↓
RAG Pipeline retrieves sources
     ↓
LLMProviderManager.generate_with_fallback()
     ↓
Try Provider 1 (Groq)
     ├─ Success? → Return response ✅
     └─ Failed? → Try Provider 2 (OpenRouter)
          ├─ Success? → Return response ✅
          └─ Failed? → Try Provider 3 (Ollama)
               ├─ Success? → Return response ✅
               └─ Failed? → Try Provider 4 (HuggingFace)
                    ├─ Success? → Return response ✅
                    └─ All failed? → Return error ❌
```

### Automatic Switching Triggers

The system automatically switches providers when:
- ⚠️ Rate limit exceeded (HTTP 429)
- ❌ Connection timeout
- ❌ API key invalid/expired
- ❌ Service unavailable (HTTP 503)
- ❌ 3 consecutive errors from same provider

### Provider Recovery

- Disabled providers are tracked
- Can be manually reset via API
- Error count resets on successful request
- Daily limits auto-reset after 24 hours

---

## 🚀 Quick Start

### Option 1: Groq Only (Fastest, 5 min setup)

```bash
# 1. Get API key: https://console.groq.com/
# 2. Add to backend/.env:
GROQ_API_KEY=gsk_your_key_here
GROQ_MODEL=llama-3.3-70b-versatile

# 3. Restart backend
cd backend && uvicorn main:app --reload
```

### Option 2: Completely Free with Ollama (No API keys)

```bash
# 1. Install Ollama: https://ollama.ai/
brew install ollama  # macOS

# 2. Pull model
ollama pull llama3.2

# 3. Start Ollama
ollama serve

# 4. No .env changes needed! System auto-detects Ollama
```

### Option 3: Maximum Reliability (All Providers)

```bash
# Configure all providers in backend/.env:

# Priority 1: Groq
GROQ_API_KEY=gsk_your_key_here
GROQ_MODEL=llama-3.3-70b-versatile

# Priority 2: OpenRouter
OPENROUTER_API_KEY=sk-or-v1-your_key_here
OPENROUTER_MODEL=meta-llama/llama-3-8b-instruct:free

# Priority 3: Ollama (local)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2

# Priority 4: HuggingFace
HUGGINGFACE_API_KEY=hf_your_token_here
HUGGINGFACE_MODEL=HuggingFaceH4/zephyr-7b-beta
```

---

## 📊 Monitoring & Testing

### Test All Providers

```bash
cd backend
python test_llm_providers.py
```

This will:
- Check each provider's availability
- Send test requests
- Verify automatic fallback works
- Show usage statistics

### Check Provider Status via API

```bash
# Get current status
curl http://localhost:8000/api/v1/providers/status

# Response example:
{
  "status": "success",
  "data": {
    "stats": {
      "groq": {"successes": 45, "failures": 2},
      "openrouter": {"successes": 0, "failures": 0},
      "ollama": {"successes": 12, "failures": 0},
      "huggingface": {"successes": 0, "failures": 0}
    },
    "available_providers": ["groq", "ollama"],
    "current_priority_order": ["groq", "openrouter", "ollama", "huggingface"]
  }
}
```

### Reset a Disabled Provider

```bash
curl -X POST http://localhost:8000/api/v1/providers/reset \
  -H "Content-Type: application/json" \
  -d '{"provider_name": "groq"}'
```

---

## 💡 Use Cases

### Development
- **Use Ollama** - Free, unlimited, private, works offline
- No API keys needed
- Perfect for testing and development

### Production (Low Traffic)
- **Use Groq** - Fast, reliable, 200 free requests/day
- Enough for ~50-100 users/day
- Upgrade to paid if needed ($0.40/million tokens)

### Production (High Traffic)
- **Combine multiple providers** - Distribute load
- **Add Ollama** as primary for cost savings
- **Use Groq/OpenRouter** for overflow

### Privacy-Sensitive Applications
- **Use Ollama only** - All processing stays local
- No data sent to external APIs
- Complete control over data

---

## 🎓 Configuration Examples

### Change Provider Priority

Edit `backend/core/config.py`:

```python
# Prioritize local Ollama for cost savings
LLM_PROVIDER_PRIORITY = ["ollama", "groq", "openrouter", "huggingface"]

# Or prioritize speed (Groq is fastest)
LLM_PROVIDER_PRIORITY = ["groq", "openrouter", "ollama", "huggingface"]
```

### Adjust Retry Settings

```python
# Increase retries before disabling provider
MAX_RETRIES_PER_PROVIDER = 5  # Default: 3

# Adjust timeout
REQUEST_TIMEOUT = 45  # Default: 30 seconds
```

### Use Different Models

```python
# Groq models
GROQ_MODEL=mixtral-8x7b-32768  # Alternative free model

# Ollama models
OLLAMA_MODEL=qwen2.5  # Better for Russian language

# OpenRouter models
OPENROUTER_MODEL=mistralai/mistral-7b-instruct:free
```

---

## 🐛 Troubleshooting

### Problem: "No LLM providers available"

**Solution:**
1. Check at least one API key is set in `.env`
2. Or install and start Ollama locally
3. Run test script: `python test_llm_providers.py`
4. Check logs for specific errors

### Problem: Groq rate limit hit

**Solution:**
- System should auto-switch to next provider
- Wait for daily reset (midnight UTC)
- Add Ollama as fallback for unlimited usage
- Consider Groq paid tier ($0.40/million tokens)

### Problem: Ollama not connecting

**Solution:**
```bash
# Check if running
ollama list

# Start if needed
ollama serve

# Test connection
curl http://localhost:11434/api/tags
```

---

## 📈 Benefits Summary

| Feature | Before | After |
|---------|--------|-------|
| **Providers** | 1 (Qwen only) | 4 (Groq, OpenRouter, Ollama, HF) |
| **Cost** | Paid API required | Completely free option available |
| **Rate Limits** | Single point of failure | Automatic fallback |
| **Reliability** | Depends on 1 provider | 4x redundancy |
| **Privacy** | All data to cloud | Local option with Ollama |
| **Offline** | Not supported | Works with Ollama |
| **Setup Time** | Complex API setup | 5 min with Groq or Ollama |

---

## 🎯 Next Steps

1. **Test the system**: `cd backend && python test_llm_providers.py`
2. **Choose your setup**: See [LLM_PROVIDERS_GUIDE.md](LLM_PROVIDERS_GUIDE.md)
3. **Configure .env**: Add your API keys or install Ollama
4. **Monitor usage**: Check `/api/v1/providers/status`
5. **Deploy**: System is production-ready!

---

## 🔗 Resources

- **Full Setup Guide**: [LLM_PROVIDERS_GUIDE.md](LLM_PROVIDERS_GUIDE.md)
- **Groq Console**: https://console.groq.com/
- **OpenRouter**: https://openrouter.ai/
- **Ollama**: https://ollama.ai/
- **HuggingFace**: https://huggingface.co/

---

**The platform now operates completely free with automatic fallback - no more worrying about API limits! 🎉**
