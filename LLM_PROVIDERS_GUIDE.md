# 🔑 LLM Providers Setup Guide

This guide explains how to configure multiple free LLM providers with automatic fallback for the Answers Platform.

## 🎯 Provider Priority Order

The system automatically tries providers in this order:
1. **Groq** (Fastest, free tier: 30 req/min, 200 req/day)
2. **OpenRouter** (Free models available)
3. **Ollama** (Local, completely free, no limits)
4. **HuggingFace** (Free tier with rate limits)

When one provider hits its limit or fails, the system automatically switches to the next available provider.

---

## 1️⃣ Groq (Recommended - Fastest Free Tier)

**Free Tier Limits:**
- 30 requests per minute
- 200 requests per day
- Models: Llama 3.3 70B, Mixtral 8x7B, Gemma 7B

### Setup Steps:

1. **Sign up**: https://console.groq.com/
2. **Get API Key**: Go to API Keys section and create a new key
3. **Add to `.env`**:
   ```bash
   GROQ_API_KEY=gsk_your_api_key_here
   GROQ_MODEL=llama-3.3-70b-versatile
   ```

**Available Free Models:**
- `llama-3.3-70b-versatile` (recommended)
- `mixtral-8x7b-32768`
- `gemma2-9b-it`

---

## 2️⃣ OpenRouter (Multiple Free Models)

**Free Tier:**
- Access to many free models
- Rate limits vary by model
- No daily cap on free models

### Setup Steps:

1. **Sign up**: https://openrouter.ai/
2. **Get API Key**: Click "Keys" → "Create Key"
3. **Add to `.env`**:
   ```bash
   OPENROUTER_API_KEY=sk-or-v1-your_api_key_here
   OPENROUTER_MODEL=meta-llama/llama-3-8b-instruct:free
   ```

**Recommended Free Models:**
- `meta-llama/llama-3-8b-instruct:free`
- `mistralai/mistral-7b-instruct:free`
- `google/gemma-7b-it:free`

---

## 3️⃣ Ollama (Local - Completely Free)

**Benefits:**
- No API keys needed
- No rate limits
- Complete privacy
- Works offline

### Setup Steps:

1. **Install Ollama**: https://ollama.ai/
   ```bash
   # macOS
   brew install ollama
   
   # Linux
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Windows
   Download from https://ollama.ai/download
   ```

2. **Pull a model**:
   ```bash
   ollama pull llama3.2
   # or
   ollama pull mistral
   # or
   ollama pull qwen2.5
   ```

3. **Start Ollama** (usually starts automatically):
   ```bash
   ollama serve
   ```

4. **Configure in `.env`**:
   ```bash
   OLLAMA_BASE_URL=http://localhost:11434
   OLLAMA_MODEL=llama3.2
   ```

**Recommended Models:**
- `llama3.2` (3B parameters, fast)
- `llama3.1` (8B parameters, better quality)
- `mistral` (7B parameters)
- `qwen2.5` (7B parameters, good for Russian)

---

## 4️⃣ Hugging Face Inference API

**Free Tier:**
- Limited requests per hour
- Model loading time may apply
- Good as last resort fallback

### Setup Steps:

1. **Sign up**: https://huggingface.co/
2. **Get API Token**: Settings → Access Tokens → Create New Token
3. **Add to `.env`**:
   ```bash
   HUGGINGFACE_API_KEY=hf_your_token_here
   HUGGINGFACE_MODEL=HuggingFaceH4/zephyr-7b-beta
   ```

**Recommended Models:**
- `HuggingFaceH4/zephyr-7b-beta`
- `mistralai/Mistral-7B-Instruct-v0.2`
- `Qwen/Qwen2.5-7B-Instruct`

---

## ⚙️ Configuration Examples

### Minimal Setup (Just Groq)
```bash
GROQ_API_KEY=gsk_your_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

### Recommended Setup (Groq + Ollama Fallback)
```bash
# Primary: Groq
GROQ_API_KEY=gsk_your_key_here
GROQ_MODEL=llama-3.3-70b-versatile

# Fallback: Local Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
```

### Maximum Reliability (All Providers)
```bash
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

## 🔧 Customizing Provider Priority

Edit `backend/core/config.py` to change the fallback order:

```python
LLM_PROVIDER_PRIORITY: List[str] = ["groq", "openrouter", "ollama", "huggingface"]
```

For example, to prioritize local Ollama:
```python
LLM_PROVIDER_PRIORITY: List[str] = ["ollama", "groq", "openrouter", "huggingface"]
```

---

## 📊 Monitoring Provider Usage

Check which providers are active and their usage stats:

```bash
curl http://localhost:8000/api/v1/providers/status
```

Response:
```json
{
  "status": "success",
  "data": {
    "stats": {
      "groq": {"successes": 45, "failures": 2, "last_used": 1234567890},
      "openrouter": {"successes": 0, "failures": 0, "last_used": null},
      "ollama": {"successes": 12, "failures": 0, "last_used": 1234567890},
      "huggingface": {"successes": 0, "failures": 0, "last_used": null}
    },
    "available_providers": ["groq", "ollama"],
    "current_priority_order": ["groq", "openrouter", "ollama", "huggingface"]
  }
}
```

---

## 🔄 Resetting a Disabled Provider

If a provider gets disabled due to errors, you can reset it:

```bash
curl -X POST http://localhost:8000/api/v1/providers/reset \
  -H "Content-Type: application/json" \
  -d '{"provider_name": "groq"}'
```

---

## 🐛 Troubleshooting

### "No LLM providers available" Error

**Problem**: All providers are unavailable.

**Solutions**:
1. Check that at least one API key is set in `.env`
2. Verify Ollama is running: `ollama list`
3. Test Groq API: https://console.groq.com/playground
4. Check logs for specific error messages

### Groq Rate Limit Hit

**Problem**: "Rate limit exceeded" error.

**Solutions**:
1. System should automatically switch to next provider
2. Wait for limit reset (daily at midnight UTC)
3. Add Ollama as fallback for unlimited local processing
4. Consider upgrading to Groq paid tier ($0.40/million tokens)

### Ollama Not Connecting

**Problem**: "Ollama not running on localhost:11434"

**Solutions**:
```bash
# Check if Ollama is running
ollama list

# Start Ollama if not running
ollama serve

# Check if port is accessible
curl http://localhost:11434/api/tags

# Restart Ollama
brew services restart ollama  # macOS
sudo systemctl restart ollama  # Linux
```

### Slow Response Times

**Problem**: Responses taking too long.

**Solutions**:
1. Use faster models (llama3.2 instead of llama3.3-70b)
2. Reduce `max_tokens` in config
3. Prioritize Groq (fastest inference)
4. Check network connection for API providers

---

## 💡 Best Practices

1. **Always have a fallback**: Configure at least 2 providers
2. **Use Ollama for development**: Free, unlimited, private
3. **Use Groq for production**: Fastest, reliable free tier
4. **Monitor usage**: Check `/api/v1/providers/status` regularly
5. **Set up alerts**: Monitor when switching to fallback providers
6. **Cache responses**: Reduces API calls (Redis caching coming soon)

---

## 📈 Cost Comparison

| Provider | Free Tier | Paid Upgrade | Cost per 1M tokens |
|----------|-----------|--------------|-------------------|
| Groq | 200 req/day | Yes | ~$0.40 |
| OpenRouter | Free models | Yes | Varies |
| Ollama | Unlimited | N/A | $0 (local) |
| HuggingFace | Limited | Yes | Varies |

**Recommendation**: Use Groq + Ollama combination for best balance of speed, cost, and reliability.

---

## 🚀 Quick Start

1. **Get Groq API key** (5 minutes): https://console.groq.com/
2. **Install Ollama** (optional, for fallback): https://ollama.ai/
3. **Update `.env`** with your keys
4. **Restart backend**: `uvicorn main:app --reload`
5. **Test**: Ask a question and check which provider was used

The system will automatically handle fallbacks - no manual intervention needed! 🎉
