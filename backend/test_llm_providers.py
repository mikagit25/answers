"""
Тестовый скрипт для проверки работы LLM провайдеров.
Запуск: python test_llm_providers.py
"""
import asyncio
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from core.llm_manager import llm_manager
from core.config import settings


async def test_provider(provider_name: str):
    """Test a single provider"""
    print(f"\n{'='*60}")
    print(f"Testing: {provider_name.upper()}")
    print(f"{'='*60}")
    
    provider = llm_manager.providers.get(provider_name)
    if not provider:
        print(f"❌ Provider '{provider_name}' not found")
        return False
    
    # Check availability
    is_available = provider.is_available()
    print(f"Available: {'✅ Yes' if is_available else '❌ No'}")
    
    if not is_available:
        return False
    
    # Test generation
    try:
        print(f"Sending test request...")
        result = await provider.generate(
            prompt="Say hello in Russian",
            system_prompt="You are a helpful assistant.",
            temperature=0.3,
            max_tokens=50,
        )
        print(f"✅ Success!")
        print(f"Response: {result[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


async def test_fallback():
    """Test automatic fallback mechanism"""
    print(f"\n{'='*60}")
    print("Testing AUTOMATIC FALLBACK mechanism")
    print(f"{'='*60}\n")
    
    try:
        result = await llm_manager.generate_with_fallback(
            prompt="What is stoicism in one sentence?",
            system_prompt="You are a philosophy expert. Be concise.",
            temperature=0.3,
            max_tokens=100,
        )
        
        print(f"✅ Fallback test successful!")
        print(f"Provider used: {result['provider']}")
        print(f"Model: {result['model']}")
        print(f"Fallback was available: {result['fallback_used']}")
        print(f"\nResponse:\n{result['response']}\n")
        return True
        
    except Exception as e:
        print(f"❌ Fallback test failed: {str(e)}")
        return False


async def show_stats():
    """Show provider statistics"""
    print(f"\n{'='*60}")
    print("PROVIDER STATISTICS")
    print(f"{'='*60}\n")
    
    stats = llm_manager.get_stats()
    
    print(f"Available providers: {', '.join(stats['available_providers'])}")
    print(f"Priority order: {' -> '.join(stats['current_priority_order'])}")
    print(f"\nUsage stats:")
    
    for provider_name, provider_stats in stats['stats'].items():
        successes = provider_stats['successes']
        failures = provider_stats['failures']
        last_used = provider_stats['last_used']
        
        status = "✅" if successes > 0 else "⚪"
        print(f"  {status} {provider_name}: {successes} successes, {failures} failures")


async def main():
    """Run all tests"""
    print("\n🧪 LLM Providers Test Suite")
    print("=" * 60)
    
    # Show configuration
    print(f"\nConfigured providers:")
    print(f"  Groq: {'✅' if settings.GROQ_API_KEY else '❌'} (API key {'set' if settings.GROQ_API_KEY else 'not set'})")
    print(f"  OpenRouter: {'✅' if settings.OPENROUTER_API_KEY else '❌'} (API key {'set' if settings.OPENROUTER_API_KEY else 'not set'})")
    print(f"  Ollama: {'✅' if settings.OLLAMA_BASE_URL else '❌'} (URL: {settings.OLLAMA_BASE_URL})")
    print(f"  HuggingFace: {'✅' if settings.HUGGINGFACE_API_KEY else '❌'} (API key {'set' if settings.HUGGINGFACE_API_KEY else 'not set'})")
    
    # Test individual providers
    results = {}
    for provider_name in settings.LLM_PROVIDER_PRIORITY:
        results[provider_name] = await test_provider(provider_name)
    
    # Test fallback mechanism
    if any(results.values()):
        await test_fallback()
    
    # Show statistics
    await show_stats()
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    
    available_count = sum(1 for v in results.values() if v)
    total_count = len(results)
    
    print(f"\nProviders working: {available_count}/{total_count}")
    
    if available_count == 0:
        print("\n⚠️  No providers available!")
        print("\nTo fix this:")
        print("1. Set at least one API key in .env file")
        print("2. Or install and start Ollama locally")
        print("3. See LLM_PROVIDERS_GUIDE.md for setup instructions")
    else:
        print("\n✅ System is ready to use!")
    
    print(f"\n{'='*60}\n")


if __name__ == "__main__":
    asyncio.run(main())
