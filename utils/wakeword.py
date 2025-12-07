# utils/wakeword.py
import threading
from utils.speech import listen, speak
from config import WAKE_WORDS

def start_wake_listener(event, wake_words=WAKE_WORDS):
    """
    Start a daemon thread that listens for the wake word and sets an Event.
    Usage:
        t = start_wake_listener(WAKE_EVENT)
    """
    def _loop():
        speak("Wake listener started")
        while True:
            txt = listen(timeout=3, phrase_time_limit=3)
            if txt and txt != "None":
                t = txt.lower()
                for w in wake_words:
                    if w in t:
                        speak("Yes Sir?")
                        event.set()
                        break
    t = threading.Thread(target=_loop, daemon=True)
    t.start()
    return t
