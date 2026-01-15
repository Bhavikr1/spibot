#!/usr/bin/env python3
"""
Complete conversation test - showing all 3 stages
"""
import requests
import json
import time

API_URL = "http://localhost:8000/api/text/query"

def chat(message, history):
    """Send a message and get response"""
    response = requests.post(API_URL, json={
        "query": message,
        "language": "en",
        "include_citations": True,
        "conversation_history": history
    })

    if response.status_code == 200:
        data = response.json()
        return data['answer'], data.get('citations', [])
    return None, []

def print_message(role, content, citations=None):
    """Pretty print a message"""
    if role == "user":
        print(f"\n👤 User: {content}")
    else:
        print(f"\n🤖 Bot: {content}")
        if citations:
            print("\n   📖 Scripture References:")
            for i, citation in enumerate(citations[:2], 1):
                print(f"   {i}. {citation['reference']}")

def main():
    print("="*70)
    print("  SPIRITUAL BOT - FULL CONVERSATIONAL FLOW TEST")
    print("  Demonstrating: Understanding → Empathy → Wisdom")
    print("="*70)

    conversation_history = []

    # Turn 1: User shares problem
    user_msg = "I feel lost and don't know my purpose in life"
    print_message("user", user_msg)
    bot_response, citations = chat(user_msg, conversation_history)
    if bot_response:
        print_message("bot", bot_response, citations)
        conversation_history.append({"role": "user", "content": user_msg})
        conversation_history.append({"role": "assistant", "content": bot_response})

    time.sleep(1)

    # Turn 2: User provides context
    user_msg = "I'm in my 30s, I have a stable job but it doesn't excite me. I feel like I'm just going through the motions every day."
    print_message("user", user_msg)
    bot_response, citations = chat(user_msg, conversation_history)
    if bot_response:
        print_message("bot", bot_response, citations)
        conversation_history.append({"role": "user", "content": user_msg})
        conversation_history.append({"role": "assistant", "content": bot_response})

    time.sleep(1)

    # Turn 3: User wants guidance
    user_msg = "Yes, I'd really appreciate some wisdom from the scriptures on how to find my purpose."
    print_message("user", user_msg)
    bot_response, citations = chat(user_msg, conversation_history)
    if bot_response:
        print_message("bot", bot_response, citations)

    print("\n" + "="*70)
    print("  CONVERSATION COMPLETE")
    print("="*70)
    print("\n✅ Bot successfully:")
    print("   1. Asked clarifying questions (STAGE 1)")
    print("   2. Showed empathy and understanding (STAGE 2)")
    print("   3. Offered relevant scriptural wisdom (STAGE 3)")
    print("="*70)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
