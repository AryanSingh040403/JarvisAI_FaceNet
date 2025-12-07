# features/alarm.py
import threading, time
from utils.speech import speak
import datetime
import winsound  # Windows only

def alarm_thread(target_ts, label='Alarm'):
    now = time.time()
    delta = target_ts - now
    if delta > 0:
        time.sleep(delta)
    for _ in range(6):
        speak(f"{label}. Time is up.")
        try:
            # beep pattern
            winsound.Beep(1200, 600)
            time.sleep(0.2)
        except Exception:
            pass

def set_alarm_hhmm(timestr: str, label='Alarm'):
    now = datetime.datetime.now()
    try:
        t = datetime.datetime.strptime(timestr, "%H:%M")
        target = now.replace(hour=t.hour, minute=t.minute, second=0, microsecond=0)
    except ValueError:
        try:
            t = datetime.datetime.strptime(timestr, "%H:%M:%S")
            target = now.replace(hour=t.hour, minute=t.minute, second=t.second, microsecond=0)
        except Exception:
            speak("Time format not recognized. Use HH:MM or HH:MM:SS.")
            return
    if target < now:
        target += datetime.timedelta(days=1)
    th = threading.Thread(target=alarm_thread, args=(target.timestamp(), label), daemon=True)
    th.start()
    return th
