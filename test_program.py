#!/usr/bin/env python3
import requests
import time
import json

def test_weather_microservice():
    base_url = "http://127.0.0.1:5000"
    endpoint = "/weather"
    
    test_cases = [
        {"city": "New York", "state": "NY", "description": "Valid city test"},
        {"city": "Los Angeles", "state": "CA", "description": "Another valid city test"},
        {"city": "Hello", "state": "CA", "description": "Invalid city test"},
        {"city": "", "state": "NY", "description": "Empty city test"},
        {"city": "Chicago", "state": "", "description": "Empty state test"}
    ]
    
    print("WEATHER MICROSERVICE TEST PROGRAM")
    print()
    
    print(f"Target URL: {base_url}{endpoint}")
    print()
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test {i}: {test_case['description']}")
        print(f"Requesting weather for: {test_case['city']}, {test_case['state']}")
        print("-" * 40)
        
        try:
            response = requests.get(
                f"{base_url}{endpoint}",
                params={
                    'city': test_case['city'],
                    'state': test_case['state']
                },
                timeout=10
            )
            
            data = response.json()
            
            print(f"HTTP Status Code: {response.status_code}")
            print(f"Response Data: {json.dumps(data, indent=2)}")
            
            if data['status'] == 'success':
                print(f"SUCCESS: Temperature in {data['city']}, {data['state']} is {data['temperature']}°F with {data['weather_type']}")
            elif data['status'] == 'failed':
                print(f"EXPECTED FAILURE: {data['message']}")
            elif data['status'] == 'error':
                print(f"ERROR: {data['message']}")
            else:
                print(f"UNKNOWN STATUS: {data}")
                
        except requests.exceptions.ConnectionError:
            print("CONNECTION ERROR: Could not connect to the microservice")
            print("Make sure the microservice is running with: python microservice_a.py")
        except requests.exceptions.Timeout:
            print("TIMEOUT: Request took too long")
        except requests.exceptions.RequestException as e:
            print(f"REQUEST ERROR: {e}")
        except json.JSONDecodeError:
            print("JSON ERROR: Could not parse response as JSON")
        except Exception as e:
            print(f"UNEXPECTED ERROR: {e}")
        
        print()
        time.sleep(1)

if __name__ == "__main__":
    test_weather_microservice()
