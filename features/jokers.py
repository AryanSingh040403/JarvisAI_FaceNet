# features/jokes.py
from utils.speech import speak
import time

JOKES = [
    "Why don't scientists trust atoms? Because they make up everything.",
    "Why did the programmer quit his job? Because he didn't get arrays.",
    "I told my computer I needed a break, and it said no problem — it would go to sleep."
]
FACTS = [
    "Honey never spoils. Archaeologists have found edible honey in ancient Egyptian tombs.",
    "Octopuses have three hearts.",
    "Bananas are berries, but strawberries are not."
]
QUOTES = [
    "The best way to predict the future is to invent it. — Alan Kay",
    "Code is like humor. When you have to explain it, it’s bad. — Cory House"
]

def tell_joke():
    speak(JOKES[int(time.time()) % len(JOKES)])

def tell_fact():
    speak(FACTS[int(time.time()) % len(FACTS)])

def tell_quote():
    speak(QUOTES[int(time.time()) % len(QUOTES)])
