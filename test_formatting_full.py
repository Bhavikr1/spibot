#!/usr/bin/env python3
import requests

API_URL = "http://localhost:8000/api/text/query"

conversation = []

print("Testing full conversation with Bhagavad Gita wisdom...")
print("="*70)

# Message 1
response1 = requests.post(API_URL, json={
    "query": "I'm stressed about work deadlines",
    "language": "en",
    "include_citations": False,
    "conversation_history": conversation
})

if response1.status_code == 200:
    bot_msg1 = response1.json()['answer']
    conversation.append({"role": "user", "content": "I'm stressed about work deadlines"})
    conversation.append({"role": "assistant", "content": bot_msg1})
    print(f"\n👤 User: I'm stressed about work deadlines")
    print(f"\n🤖 Bot: {bot_msg1}\n")

# Message 2 - User provides context
response2 = requests.post(API_URL, json={
    "query": "It's because my boss keeps adding more tasks and I can't say no",
    "language": "en",
    "include_citations": True,
    "conversation_history": conversation
})

if response2.status_code == 200:
    bot_msg2 = response2.json()['answer']
    print(f"👤 User: It's because my boss keeps adding more tasks and I can't say no")
    print(f"\n🤖 Bot:\n{bot_msg2}\n")
    print("="*70)
    
    # Check for formatting issues
    issues = []
    if '*' in bot_msg2:
        asterisk_count = bot_msg2.count('*')
        # Allow for citations like Bhagavad Gita 2.47*
        if asterisk_count > 2:
            issues.append(f"⚠️  Too many asterisks found: {asterisk_count}")
    
    if not issues:
        print("\n✅ CLEAN FORMATTING - No asterisks or word-smashing!")
    else:
        print("\n❌ ISSUES:")
        for issue in issues:
            print(f"   {issue}")
else:
    print(f"Error: {response2.status_code}")
