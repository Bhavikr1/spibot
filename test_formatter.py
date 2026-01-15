#!/usr/bin/env python3
"""
Test the new response formatter
"""
import asyncio
import sys
import os
from dotenv import load_dotenv

# Add backend to path
backend_path = os.path.join(os.path.dirname(__file__), 'spiritual-voice-bot', 'backend')
sys.path.insert(0, backend_path)

# Load environment variables from backend .env
env_path = os.path.join(backend_path, '.env')
load_dotenv(env_path)

from llm.formatter import ResponseFormatter, QueryRefiner
from config import settings


async def test_formatter():
    """Test the response formatter"""
    print("=" * 60)
    print("Testing Response Formatter")
    print("=" * 60)

    formatter = ResponseFormatter(settings.GEMINI_API_KEY)

    if not formatter.available:
        print("❌ Formatter not available - check GEMINI_API_KEY")
        return

    # Example long text without proper breaks (similar to the issue)
    long_text = """Greetings."Salutations to Thee, in front and behind! Salutations to Thee onevery side! O All! Thou infinite in power and prowess, pervadest all; wherefore Thou art all."omnipotence of the Divine. Krishna, in his universal form, is acknowledged as being present in all directions and encompassing everything.divine in all aspects of existence. How might recognizing the divine in all things shift your perspective?"""

    print("\n📝 ORIGINAL TEXT (hard to read):")
    print("-" * 60)
    print(long_text)
    print()

    print("\n🔄 Formatting...")
    formatted_text = await formatter.format_response(long_text)

    print("\n✅ FORMATTED TEXT (easy to read):")
    print("-" * 60)
    print(formatted_text)
    print()

    # Count paragraph breaks
    original_breaks = long_text.count('\n\n')
    formatted_breaks = formatted_text.count('\n\n')

    print(f"\n📊 Stats:")
    print(f"   Original paragraph breaks: {original_breaks}")
    print(f"   Formatted paragraph breaks: {formatted_breaks}")
    print(f"   ✓ Improvement: {formatted_breaks - original_breaks} additional breaks")


async def test_refiner():
    """Test the query refiner"""
    print("\n" + "=" * 60)
    print("Testing Query Refiner")
    print("=" * 60)

    refiner = QueryRefiner(settings.GEMINI_API_KEY)

    if not refiner.available:
        print("❌ Refiner not available - check GEMINI_API_KEY")
        return

    test_queries = [
        "hi",
        "I feel lost in life",
        "What should I do when people are mean to me?",
        "How to find peace?",
    ]

    for query in test_queries:
        print(f"\n📝 Original query: \"{query}\"")
        refined = await refiner.refine_query(query, "en")
        print(f"✅ Refined query: \"{refined}\"")


async def main():
    """Run all tests"""
    await test_formatter()
    await test_refiner()
    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
