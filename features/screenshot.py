# features/screenshot.py
from PIL import ImageGrab
from pathlib import Path
from datetime import datetime
from utils.speech import speak
from config import FILES_DIR

def take_screenshot():
    now = datetime.now().strftime('%Y%m%d_%H%M%S')
    p = FILES_DIR / f'screenshot_{now}.png'
    img = ImageGrab.grab()
    img.save(str(p))
    speak(f"Screenshot saved to {p}")
    return str(p)
