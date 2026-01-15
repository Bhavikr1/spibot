#!/usr/bin/env python3
"""
Test script for conversational spiritual bot
"""
import requests
import json

API_URL = "http://localhost:8000/api/text/query"

def test_conversation():
    """Test a multi-turn conversation"""

    print("="*60)
    print("Testing Conversational Spiritual Bot")
    print("="*60)

    conversation_history = []

    # Test 1: Greeting
    print("\n[Test 1: Greeting]")
    print("User: hi")
    response = requests.post(API_URL, json={
        "query": "hi",
        "language": "en",
        "include_citations": False,
        "conversation_history": conversation_history
    })

    if response.status_code == 200:
        data = response.json()
        bot_response = data['answer']
        print(f"Bot: {bot_response}")

        # Update conversation history
        conversation_history.append({"role": "user", "content": "hi"})
        conversation_history.append({"role": "assistant", "content": bot_response})

    # Test 2: User shares problem
    print("\n[Test 2: User shares problem - expecting clarifying questions]")
    print("User: I am very stressed")
    response = requests.post(API_URL, json={
        "query": "I am very stressed",
        "language": "en",
        "include_citations": False,
        "conversation_history": conversation_history
    })

    if response.status_code == 200:
        data = response.json()
        bot_response = data['answer']
        print(f"Bot: {bot_response}")

        # Update conversation history
        conversation_history.append({"role": "user", "content": "I am very stressed"})
        conversation_history.append({"role": "assistant", "content": bot_response})

    # Test 3: User provides more context
    print("\n[Test 3: User provides context - expecting empathy and wisdom]")
    print("User: It's my work. I have too many deadlines and my boss keeps adding more")
    response = requests.post(API_URL, json={
        "query": "It's my work. I have too many deadlines and my boss keeps adding more",
        "language": "en",
        "include_citations": True,
        "conversation_history": conversation_history
    })

    if response.status_code == 200:
        data = response.json()
        bot_response = data['answer']
        citations = data.get('citations', [])

        print(f"Bot: {bot_response}")

        if citations:
            print("\nScripture References:")
            for i, citation in enumerate(citations[:2], 1):
                print(f"\n{i}. {citation['reference']}")
                print(f"   \"{citation['text'][:100]}...\"")

    print("\n" + "="*60)
    print("Conversation Test Complete!")
    print("="*60)

if __name__ == "__main__":
    try:
        test_conversation()
    except Exception as e:
        print(f"Error: {e}")
