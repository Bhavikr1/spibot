"""
Test script for API endpoints
"""
import requests
import json

API_URL = "http://localhost:8000"


def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    response = requests.get(f"{API_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()


def test_text_query():
    """Test text query endpoint"""
    print("Testing text query endpoint...")
    payload = {
        "query": "What does the Bhagavad Gita say about controlling the mind?",
        "language": "en",
        "include_citations": True
    }
    response = requests.post(f"{API_URL}/api/text/query", json=payload)
    print(f"Status: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"Answer: {data['answer']}")
        print(f"\nCitations ({len(data['citations'])}):")
        for citation in data['citations']:
            print(f"  - {citation['reference']}: {citation['text'][:100]}...")
        print(f"\nConfidence: {data['confidence']:.2f}")
    else:
        print(f"Error: {response.text}")
    print()


def test_scripture_search():
    """Test scripture search endpoint"""
    print("Testing scripture search endpoint...")
    params = {
        "query": "mind control",
        "language": "en",
        "limit": 3
    }
    response = requests.get(f"{API_URL}/api/scripture/search", params=params)
    print(f"Status: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"Found {data['count']} results:")
        for result in data['results']:
            print(f"  - {result['reference']}: {result['text'][:100]}...")
            print(f"    Score: {result['score']:.3f}")
    else:
        print(f"Error: {response.text}")
    print()


def test_hindi_query():
    """Test Hindi query"""
    print("Testing Hindi query...")
    payload = {
        "query": "मन को कैसे नियंत्रित करें?",
        "language": "hi",
        "include_citations": True
    }
    response = requests.post(f"{API_URL}/api/text/query", json=payload)
    print(f"Status: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"Answer: {data['answer']}")
        print(f"Citations: {len(data['citations'])}")
    else:
        print(f"Error: {response.text}")
    print()


def main():
    """Run all tests"""
    print("=" * 60)
    print("Spiritual Voice Bot - API Tests")
    print("=" * 60)
    print()

    try:
        # Test basic connectivity
        test_health()

        # Test text queries
        test_text_query()

        # Test search
        test_scripture_search()

        # Test Hindi
        test_hindi_query()

        print("=" * 60)
        print("All tests completed!")
        print("=" * 60)

    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to API")
        print("Please ensure the backend is running at", API_URL)
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
