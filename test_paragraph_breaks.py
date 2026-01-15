#!/usr/bin/env python3
"""
Test the paragraph break formatter
"""
import sys
import os

# Add backend to path
backend_path = os.path.join(os.path.dirname(__file__), 'spiritual-voice-bot', 'backend')
sys.path.insert(0, backend_path)

from llm.formatter import ensure_paragraph_breaks

# Test with the actual problematic text from the screenshot
test_text1 = """Greetings.Salutations to Thee, in front and behind! Salutations to Thee onevery side! O All! Thou infinite in power and prowess, pervadest all; wherefore Thou art all.omnipotence of the Divine. Krishna, in his universal form, is acknowledged as being present in all directions and encompassing everything.divine in all aspects of existence. How might recognizing the divine in all things shift your perspective?"""

test_text2 = """Iacknowledgethat you are feeling upset.Krishna says: "Sanjaya said To him who was thus overcome with pity andwho was despondent, with eyes full of tears and agitated, Madhusudana (the destroyer of Madhu) or Krishna spoke these words."This verse describes Arjuna's state of distress and emotional turmoil on the battlefield. Krishna is about to offer guidance to Arjuna, who is overwhelmed with sorrow and confusion.This verse reminds us that even in moments of deep upset, divine guidance and wisdom can be found. Perhaps reflecting on what is causing your upset can help you find clarity."""

print("=" * 80)
print("Testing Paragraph Break Formatter")
print("=" * 80)

print("\n📝 TEST 1: First message from screenshot")
print("-" * 80)
print("ORIGINAL (hard to read):")
print(test_text1)
print("\n" + "=" * 80)
print("FORMATTED (with breaks):")
formatted1 = ensure_paragraph_breaks(test_text1)
print(formatted1)
print("\n" + "=" * 80)
print(f"✓ Original breaks: {test_text1.count(chr(10) + chr(10))}")
print(f"✓ Formatted breaks: {formatted1.count(chr(10) + chr(10))}")

print("\n" + "=" * 80)
print("\n📝 TEST 2: Second message from screenshot")
print("-" * 80)
print("ORIGINAL (hard to read):")
print(test_text2)
print("\n" + "=" * 80)
print("FORMATTED (with breaks):")
formatted2 = ensure_paragraph_breaks(test_text2)
print(formatted2)
print("\n" + "=" * 80)
print(f"✓ Original breaks: {test_text2.count(chr(10) + chr(10))}")
print(f"✓ Formatted breaks: {formatted2.count(chr(10) + chr(10))}")

print("\n" + "=" * 80)
print("✅ Tests completed!")
print("=" * 80)
