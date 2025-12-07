# features/whatsapp.py
import pywhatkit
from utils.speech import speak
import datetime

def send_whatsapp_pywhatkit(number: str, message: str, delay_sec: int = 10):
    """
    number should be in format +<countrycode><number>, e.g. +9199xxxxxxx
    pywhatkit opens web.whatsapp; requires QR login first.
    """
    try:
        now = datetime.datetime.now() + datetime.timedelta(seconds=delay_sec+10)
        h, m = now.hour, now.minute
        pywhatkit.sendwhatmsg(number, message, h, m, wait_time=15, tab_close=True)
        speak("WhatsApp message scheduled, check your browser.")
    except Exception as e:
        print("WhatsApp error:", e)
        speak("Failed to send WhatsApp message.")
