#!/usr/bin/env python3
import requests

API_URL = "http://localhost:8000/api/text/query"

print("Testing formatting improvements...")
print("="*70)

response = requests.post(API_URL, json={
    "query": "the deadlines are too close and i cant complete it on time",
    "language": "en",
    "include_citations": False,
    "conversation_history": []
})

if response.status_code == 200:
    data = response.json()
    answer = data['answer']
    
    print("\n🤖 Bot Response:\n")
    print(answer)
    print("\n" + "="*70)
    
    # Check for issues
    issues = []
    if '*' in answer and not answer.count('*') == 0:
        issues.append("⚠️  Contains asterisks (*)")
    if '  ' in answer:
        issues.append("⚠️  Contains double spaces")
    
    # Check for common word-smashing patterns
    words_to_check = ['thisaffecting', 'encouragesus', 'itdifficult']
    for word in words_to_check:
        if word in answer.lower():
            issues.append(f"⚠️  Word smashing detected: {word}")
    
    if issues:
        print("\n❌ FORMATTING ISSUES FOUND:")
        for issue in issues:
            print(f"   {issue}")
    else:
        print("\n✅ FORMATTING LOOKS GOOD!")
else:
    print(f"Error: {response.status_code}")
