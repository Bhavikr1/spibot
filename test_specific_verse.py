#!/usr/bin/env python3
import requests
import json

API_URL = "http://localhost:8000/api/text/query"

conversation_history = []

# Test with a query that should definitely match Karma Yoga
print("Testing: Stress about work outcomes")
print("="*70)

response = requests.post(API_URL, json={
    "query": "I'm very anxious about the results of my work projects. What does Bhagavad Gita say?",
    "language": "en",
    "include_citations": True,
    "conversation_history": []
})

if response.status_code == 200:
    data = response.json()
    print(f"\n🤖 Bot Response:\n{data['answer']}\n")
    
    if data.get('citations'):
        print("\n📖 Scripture Citations:")
        for i, citation in enumerate(data['citations'][:3], 1):
            print(f"\n{i}. {citation['reference']} (relevance: {citation['score']:.2f})")
            print(f"   \"{citation['text'][:150]}...\"")
    else:
        print("\n⚠️ No citations provided!")
else:
    print(f"Error: {response.status_code}")

print("\n" + "="*70)
