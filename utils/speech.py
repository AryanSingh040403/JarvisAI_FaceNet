# utils/speech.py
import pyttsx3
import speech_recognition as sr
import platform
import traceback

engine = pyttsx3.init('sapi5' if platform.system() == 'Windows' else None)
voices = engine.getProperty('voices')
if voices:
    engine.setProperty('voice', voices[0].id)

_recognizer = sr.Recognizer()
_recognizer.energy_threshold = 300
_recognizer.dynamic_energy_threshold = True

def speak(text: str):
    """Speak text using pyttsx3 (synchronous)."""
    print("[Jarvis]", text)
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception:
        print("TTS error:")
        traceback.print_exc()

def listen(timeout=5, phrase_time_limit=8) -> str:
    """
    Listen via microphone and return recognized string.
    Returns "None" string on failure for easy checks consistent with existing code.
    """
    with sr.Microphone() as src:
        try:
            _recognizer.adjust_for_ambient_noise(src, duration=0.5)
        except Exception:
            pass
        try:
            audio = _recognizer.listen(src, timeout=timeout, phrase_time_limit=phrase_time_limit)
        except sr.WaitTimeoutError:
            return "None"
    try:
        text = _recognizer.recognize_google(audio, language='en-in')
        print("User:", text)
        return text
    except Exception:
        return "None"
