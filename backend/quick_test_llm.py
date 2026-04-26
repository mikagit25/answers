#!/usr/bin/env python3
"""
Быстрый тест LLM провайдеров без полной настройки проекта.
Проверяет только API ключи и подключение к провайдерам.
"""
import asyncio
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

from core.llm_manager import llm_manager
from core.config import settings


async def test_providers():
    """Test configured providers"""
    print("\n" + "="*60)
    print("🧪 Testing LLM Providers")
    print("="*60 + "\n")
    
    # Show configuration
    print("📋 Configuration:")
    print(f"  Groq API Key: {'✅ Set' if settings.GROQ_API_KEY else '❌ Not set'}")
    print(f"  OpenRouter API Key: {'✅ Set' if settings.OPENROUTER_API_KEY else '❌ Not set'}")
    print(f"  Ollama URL: {settings.OLLAMA_BASE_URL}")
    print(f"  HuggingFace API Key: {'✅ Set' if settings.HUGGINGFACE_API_KEY else '❌ Not set'}")
    print()
    
    # Test each provider
    for provider_name in settings.LLM_PROVIDER_PRIORITY:
        provider = llm_manager.providers.get(provider_name)
        if not provider:
            continue
            
        print(f"\n{'─'*60}")
        print(f"Testing: {provider_name.upper()}")
        print(f"{'─'*60}")
        
        is_available = provider.is_available()
        print(f"Available: {'✅ Yes' if is_available else '❌ No'}")
        
        if not is_available:
            continue
        
        # Test generation
        try:
            print("Sending test request...")
            result = await provider.generate(
                prompt="Say hello in Russian and explain stoicism in one sentence",
                system_prompt="You are a helpful assistant. Be concise.",
                temperature=0.3,
                max_tokens=100,
            )
            print(f"✅ Success!")
            print(f"\nResponse:\n{result}\n")
            
        except Exception as e:
            print(f"❌ Error: {type(e).__name__}: {str(e)}")
    
    # Test fallback mechanism
    print(f"\n{'='*60}")
    print("🔄 Testing Automatic Fallback")
    print(f"{'='*60}\n")
    
    try:
        result = await llm_manager.generate_with_fallback(
            prompt="What is the meaning of life according to stoicism?",
            system_prompt="You are a philosophy expert. Answer concisely.",
            temperature=0.3,
            max_tokens=150,
        )
        
        print(f"✅ Fallback test successful!")
        print(f"Provider used: {result['provider']}")
        print(f"Model: {result['model']}")
        print(f"Fallback was available: {result['fallback_used']}")
        print(f"\nResponse:\n{result['response']}\n")
        
    except Exception as e:
        print(f"❌ Fallback test failed: {type(e).__name__}: {str(e)}")
    
    # Show stats
    print(f"\n{'='*60}")
    print("📊 Provider Statistics")
    print(f"{'='*60}\n")
    
    stats = llm_manager.get_stats()
    print(f"Available providers: {', '.join(stats['available_providers'])}")
    print(f"Priority order: {' → '.join(stats['current_priority_order'])}")


if __name__ == "__main__":
    print("\n🚀 Quick LLM Provider Test")
    print("This will test your API keys without full project setup\n")
    
    try:
        asyncio.run(test_providers())
        print("\n" + "="*60)
        print("✅ Test complete!")
        print("="*60 + "\n")
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Test failed with error: {e}")
        sys.exit(1)
