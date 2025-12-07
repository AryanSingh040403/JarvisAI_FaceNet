# config.py
from pathlib import Path
import os

BASE = Path(__file__).parent
DATA = BASE / 'data'
DATA.mkdir(exist_ok=True)

APPS_FILE = DATA / 'apps.json'
NOTES_FILE = DATA / 'notes.json'
EMB_DIR = BASE / 'embeddings'
KNOWN_DIR = BASE / 'known_faces'
FILES_DIR = BASE / 'files'

EMB_DIR.mkdir(parents=True, exist_ok=True)
KNOWN_DIR.mkdir(parents=True, exist_ok=True)
FILES_DIR.mkdir(parents=True, exist_ok=True)

# API Keys (set as environment variables)
WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY', '')
NEWS_API_KEY = os.environ.get('NEWS_API_KEY', '')
EMAIL_USER = os.environ.get('EMAIL_USER', '')
EMAIL_PASS = os.environ.get('EMAIL_PASS', '')
TWILIO_SID = os.environ.get('TWILIO_SID', '')
TWILIO_TOKEN = os.environ.get('TWILIO_TOKEN', '')
TWILIO_WHATSAPP_FROM = os.environ.get('TWILIO_WHATSAPP_FROM', '')

# Wake words
WAKE_WORDS = ('hey jarvis', 'ok jarvis', 'jarvis')

# Face recognition threshold (cosine similarity). Tune between 0.55-0.65.
FACE_MATCH_THRESHOLD = 0.58
