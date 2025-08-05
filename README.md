Weather Microservice - Communication Contract

Microservice A: Weather Data Service
For: Andrew Schaaf
Status: Complete

Overview
This microservice provides current weather information for any city and state in the United States. It uses the Open-Meteo API to fetch real-time weather data.

Communication Contract

How to REQUEST Data from the Microservice

Endpoint: GET /weather  
Base URL: http://127.0.0.1:5000

Required Parameters:
- city (string): The name of the city
- state (string): The state name or abbreviation

Example Request:
```python
import requests

# Make a request to get weather for New York, NY
response = requests.get('http://127.0.0.1:5000/weather', 
                       params={'city': 'New York', 'state': 'NY'})

# The response will be JSON data
data = response.json()
```

Alternative using curl:
```bash
curl "http://127.0.0.1:5000/weather?city=New+York&state=NY"
```

How to RECEIVE Data from the Microservice

Successful Response (HTTP 200):
```json
{
  "status": "success",
  "city": "New York",
  "state": "NY",
  "temperature": 77.1,
  "weather_type": "clear sky"
}
```

Failed Response (HTTP 404):
```json
{
  "status": "failed",
  "message": "City not found. Please check the city and state names."
}
```

Error Response (HTTP 500):
```json
{
  "status": "error",
  "message": "An unexpected error occurred: [error details]"
}
```

Response Fields:
- status: "success", "failed", or "error"
- city: The city name
- state: The state you provided
- temperature: Current temperature in Fahrenheit
- weather_type: Human-readable weather description
- message: Error message

UML Sequence Diagram

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐    ┌─────────────┐
│   Client    │    │ Microservice │    │Geocoding API│    │Weather API  │
│  Program    │    │     A        │    │(Open-Meteo) │    │(Open-Meteo) │
└──────┬──────┘    └──────┬───────┘    └──────┬──────┘    └──────┬──────┘
       │                  │                   │                   │
       │ GET /weather     │                   │                   │
       │ city, state      │                   │                   │
       │─────────────────>│                   │                   │
       │                  │                   │                   │
       │                  │ GET /search       │                   │
       │                  │ name=city         │                   │
       │                  │──────────────────>│                   │
       │                  │                   │                   │
       │                  │ coordinates       │                   │
       │                  │<──────────────────│                   │
       │                  │                   │                   │
       │                  │ GET /forecast     │                   │
       │                  │ lat, lon          │                   │
       │                  │──────────────────────────────────────>│
       │                  │                   │                   │
       │                  │ weather data      │                   │
       │                  │<──────────────────────────────────────│
       │                  │                   │                   │
       │ JSON response    │                   │                   │
       │ with weather     │                   │                   │
       │<─────────────────│                   │                   │
       │                  │                   │                   │
```

Integration Instructions

1. Start the Microservice:
   ```bash
   cd /path/to/microservice
   python microservice_a.py
   ```

2. Make API Calls:
   ```python
   import requests
   
   def get_weather(city, state):
       try:
           response = requests.get('http://127.0.0.1:5000/weather', 
                                 params={'city': city, 'state': state})
           data = response.json()
           
           if data['status'] == 'success':
               return f"Temperature in {data['city']}, {data['state']}: {data['temperature']}°F, {data['weather_type']}"
           else:
               return f"Error: {data['message']}"
       except requests.exceptions.RequestException as e:
           return f"Connection error: {e}"
   
   # Example usage
   print(get_weather("New York", "NY"))
   print(get_weather("Los Angeles", "CA"))
   ```
