# features/news.py
import requests
from config import NEWS_API_KEY
from utils.speech import speak

def read_news(country='in', n=5):
    if not NEWS_API_KEY:
        speak("News API key not configured.")
        return
    url = f"https://newsapi.org/v2/top-headlines?country={country}&pageSize={n}&apiKey={NEWS_API_KEY}"
    try:
        r = requests.get(url, timeout=6).json()
        articles = r.get('articles', [])
        if not articles:
            speak("No news found.")
            return
        speak("Top headlines:")
        for a in articles:
            t = a.get('title', '')
            if t:
                speak(t)
    except Exception as e:
        print("News error:", e)
        speak("Failed to fetch news.")
