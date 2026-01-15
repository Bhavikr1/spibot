#!/usr/bin/env python3
import requests

API_URL = "http://localhost:8000/api/text/query"

print("Testing Bhagavad Gita response formatting...")
print("="*70)

response = requests.post(API_URL, json={
    "query": "What does Bhagavad Gita say about not being attached to results of work?",
    "language": "en",
    "include_citations": True,
    "conversation_history": []
})

if response.status_code == 200:
    data = response.json()
    answer = data['answer']
    
    print(f"\n🤖 Bot Response:\n")
    print(answer)
    print("\n" + "="*70)
    
    # Check formatting
    issues = []
    
    # Check for asterisks (excluding citations)
    asterisk_count = answer.count('*')
    if asterisk_count > 0:
        issues.append(f"⚠️  Asterisks found: {asterisk_count}")
    
    # Check for proper Gita references
    if 'Bhagavad Gita' in answer and ('2.47' in answer or '2.48' in answer):
        print("\n✅ CONTAINS SPECIFIC BHAGAVAD GITA VERSE!")
    
    # Check spacing
    bad_patterns = ['  ', 'encouragesus', 'thisaffecting', 'itdifficult']
    for pattern in bad_patterns:
        if pattern in answer.lower():
            issues.append(f"⚠️  Spacing issue: '{pattern}'")
    
    if not issues:
        print("✅ CLEAN, WELL-FORMATTED RESPONSE!")
    else:
        print("\n❌ FORMATTING ISSUES:")
        for issue in issues:
            print(f"   {issue}")
    
    # Show citations
    if data.get('citations'):
        print(f"\n📖 Citations: {len(data['citations'])} verses")
else:
    print(f"Error: {response.status_code}")
