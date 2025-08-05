import os
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

BASE_URL = "https://api.open-meteo.com/v1/forecast"

@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    state = request.args.get('state')

    if not city or not state:
        return jsonify({"status": "error", "message": "City and state are required."}), 400

    try:
        geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"
        geocoding_params = {
            'name': city,
            'count': 1,
            'language': 'en',
            'format': 'json'
        }
        
        geo_response = requests.get(geocoding_url, params=geocoding_params)
        geo_response.raise_for_status()
        geo_data = geo_response.json()
        
        if not geo_data.get('results'):
            return jsonify({
                "status": "failed", 
                "message": "City not found. Please check the city and state names."
            }), 404
        
        location = geo_data['results'][0]
        latitude = location['latitude']
        longitude = location['longitude']
        city_name = location['name']
        
        weather_params = {
            'latitude': latitude,
            'longitude': longitude,
            'current': 'temperature_2m,weather_code',
            'temperature_unit': 'fahrenheit',
            'timezone': 'auto'
        }
        
        weather_response = requests.get(BASE_URL, params=weather_params)
        weather_response.raise_for_status()
        weather_data = weather_response.json()
        
        current = weather_data['current']
        temperature = current['temperature_2m']
        weather_code = current['weather_code']
        
        weather_descriptions = {
            0: "clear sky",
            1: "mainly clear",
            2: "partly cloudy",
            3: "overcast",
            45: "foggy",
            48: "depositing rime fog",
            51: "light drizzle",
            53: "moderate drizzle",
            55: "dense drizzle",
            61: "slight rain",
            63: "moderate rain",
            65: "heavy rain",
            71: "slight snow",
            73: "moderate snow",
            75: "heavy snow",
            77: "snow grains",
            80: "slight rain showers",
            81: "moderate rain showers",
            82: "violent rain showers",
            85: "slight snow showers",
            86: "heavy snow showers",
            95: "thunderstorm",
            96: "thunderstorm with slight hail",
            99: "thunderstorm with heavy hail"
        }
        
        weather_type = weather_descriptions.get(weather_code, "unknown")
        
        return jsonify({
            "status": "success",
            "city": city_name,
            "state": state,
            "temperature": round(temperature, 1),
            "weather_type": weather_type
        })

    except requests.exceptions.HTTPError as err:
        return jsonify({"status": "error", "message": f"An API error occurred: {err}"}), 500
    
    except Exception as e:
        return jsonify({"status": "error", "message": f"An unexpected error occurred: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
