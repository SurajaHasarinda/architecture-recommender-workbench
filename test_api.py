"""
Example script to test the Architecture Recommendation API
Run this after starting the FastAPI server
"""

import requests
import json

# API endpoint
API_URL = "http://localhost:8000/api/recommend-architecture"

# Example test cases
test_cases = [
    {
        "name": "Startup MVP",
        "context": "I'm building a simple e-commerce application for a startup with 3 developers. We need to launch an MVP quickly within 3 months. Expected user base is around 1000 users initially. Budget is limited."
    },
    {
        "name": "Large Enterprise System",
        "context": "We are developing a large-scale enterprise resource planning system for a corporation with 50+ developers. The system needs to handle millions of transactions daily, support multiple independent business units, and allow different teams to work autonomously. High availability is critical, and we need to scale different components independently."
    },
    {
        "name": "IoT Data Platform",
        "context": "Building a real-time IoT data processing platform that collects data from thousands of sensors, processes events in real-time, and sends notifications to users. The system needs to handle unpredictable spikes in sensor data and integrate with multiple third-party analytics services."
    },
    {
        "name": "Seasonal E-commerce",
        "context": "We're creating an online store that has very seasonal traffic - almost no traffic most of the year but huge spikes during holiday seasons. We want to minimize infrastructure costs during low-traffic periods but scale automatically during peak times. Development team is small (2 developers) with limited DevOps experience."
    }
]


def test_recommendation(test_case):
    """Test a single recommendation request"""
    print(f"\n{'='*80}")
    print(f"Test Case: {test_case['name']}")
    print(f"{'='*80}")
    print(f"\nContext: {test_case['context']}")
    print("\nSending request...")
    
    try:
        response = requests.post(
            API_URL,
            json={"context": test_case['context']},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✓ SUCCESS")
            print(f"\nSelected Architecture: {result['selectedArchitecture']}")
            print(f"\nExplanation:\n{result['explanation']}")
            print(f"\nMermaid Diagram Code:\n{result['diagramCode']}")
        else:
            print(f"\n✗ ERROR: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("\n✗ ERROR: Could not connect to the API. Is the server running?")
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")


def test_health():
    """Test health endpoint"""
    print("\n" + "="*80)
    print("Testing Health Endpoint")
    print("="*80)
    
    try:
        response = requests.get("http://localhost:8000/api/health")
        if response.status_code == 200:
            print("\n✓ Health check passed")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"\n✗ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")


if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════════╗
║       Architecture Recommendation API - Test Script             ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    
    # Test health first
    test_health()
    
    # Run test cases
    for test_case in test_cases:
        test_recommendation(test_case)
        input("\nPress Enter to continue to next test case...")
    
    print("\n" + "="*80)
    print("All tests completed!")
    print("="*80)
