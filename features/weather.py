# features/weather.py
import requests
from config import WEATHER_API_KEY
from utils.speech import speak

def get_weather(city: str):
    if not WEATHER_API_KEY:
        speak("Weather API key not configured.")
        return
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    try:
        r = requests.get(url, timeout=6).json()
        if r.get("cod") != 200:
            speak(r.get("message", "Weather error."))
            return
        t = r['main']['temp']
        desc = r['weather'][0]['description']
        speak(f"{city} temperature is {t} degrees Celsius with {desc}.")
    except Exception as e:
        print("Weather error:", e)
        speak("Failed to fetch weather.")
