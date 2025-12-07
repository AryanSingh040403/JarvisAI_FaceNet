# main_jarvis.py
import threading, time, os
from utils.speech import speak, listen
from utils.wakeword import start_wake_listener
from facenet_embedder import model, transform, image_to_embedding
from pathlib import Path
import numpy as np
import cv2
import torch

from config import EMB_DIR, FACE_MATCH_THRESHOLD
from utils.app_launcher import open_app
from features import notes, alarm, whatsapp, weather, news, system_control, screenshot, jokes

WAKE_EVENT = threading.Event()
start_wake_listener(WAKE_EVENT)

# load embeddings database for identities in embeddings/
EMB_DIR = Path('embeddings')
face_db = {}
for p in EMB_DIR.glob('*.npz'):
    name = p.stem
    d = np.load(p, allow_pickle=True)
    face_db[name] = {'embs': d['embeddings'], 'paths': d['paths']}

def recognize_frame(frame, threshold=FACE_MATCH_THRESHOLD):
    """Return (name, score) if matched, else (None, score)."""
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    from PIL import Image
    im = Image.fromarray(img)
    x = transform(im).unsqueeze(0).to(model.device if hasattr(model, 'device') else ('cuda' if torch.cuda.is_available() else 'cpu'))
    with torch.no_grad():
        emb = model(x).cpu().numpy().flatten()
    best_name = None
    best_score = -1
    for name, data in face_db.items():
        embs = data['embs']
        sims = embs @ emb / (np.linalg.norm(embs, axis=1)*np.linalg.norm(emb)+1e-10)
        idx = sims.argmax()
        if sims[idx] > best_score:
            best_score = sims[idx]
            best_name = name
    if best_score > threshold:
        return best_name, float(best_score)
    return None, float(best_score)

speak("Jarvis online. Say the wake word to begin.")

while True:
    WAKE_EVENT.wait()
    speak("Listening for your command.")
    q = listen(timeout=6, phrase_time_limit=12)
    if not q or q == "None":
        speak("I did not hear that.")
        WAKE_EVENT.clear()
        continue
    ql = q.lower().strip()
    print("Command:", ql)

    # Face greeting
    if any(x in ql for x in ("greet me","who is there","recognize","who's there")):
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()
        if not ret:
            speak("Camera error")
        else:
            name, score = recognize_frame(frame)
            if name:
                speak(f"Hello {name}. Score {score:.2f}")
            else:
                speak("Unknown person detected.")

    # Create folder/file
    elif "create folder" in ql or ql.startswith("create folder"):
        parts = q.split(" ", 2)
        if len(parts) >= 3:
            path = parts[2].strip().strip('"')
            Path(path).mkdir(parents=True, exist_ok=True)
            speak(f"Folder created at {path}")
        else:
            speak("Please tell me the folder path.")

    elif "create file" in ql or ql.startswith("create file"):
        parts = q.split(" ", 2)
        if len(parts) >= 3:
            path = parts[2].strip().strip('"')
            p = Path(path)
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text("")
            speak(f"File created at {path}")
        else:
            speak("Please tell me the file path.")

    # Open app by name
    elif ql.startswith("open ") or ql.startswith("launch "):
        name = ql.replace("open", "").replace("launch", "").strip()
        if name:
            open_app(name)
        else:
            speak("Which app should I open?")

    # Play a specific song or play music
    elif "play song" in ql or ("play" in ql and "music" in ql):
        # If user says "play <song name>" we attempt web search + open youtube
        if "play song" in ql and not "music" in ql:
            song = ql.replace("play song", "").strip()
            if song:
                speak(f"Playing {song} on YouTube")
                import webbrowser
                webbrowser.open(f"https://www.youtube.com/results?search_query={song.replace(' ','+')}")
            else:
                speak("Which song?")
        else:
            music_dir = Path.home() / "Music"
            files = list(music_dir.glob("*.*"))
            if files:
                os.startfile(str(files[0]))
                speak("Playing music")
            else:
                speak("No music found in your Music folder.")

    # Time
    elif "time" in ql:
        from datetime import datetime
        speak(datetime.now().strftime("%H:%M:%S"))

    # Screenshots
    elif "screenshot" in ql or "take screenshot" in ql:
        screenshot.take_screenshot()

    # Alarm
    elif "set alarm" in ql or "alarm" in ql:
        import re
        m = re.search(r"(\d{1,2}:\d{2}(?::\d{2})?)", ql)
        if m:
            alarm.set_alarm_hhmm(m.group(1))
            speak("Alarm set.")
        else:
            speak("Say the time as HH:MM")

    # Notes
    elif "note" in ql or "remember" in ql:
        speak("What should I note?")
        txt = listen(timeout=8)
        if txt and txt != "None":
            notes.add_note(txt)
            speak("Note saved.")

    # WhatsApp
    elif "whatsapp" in ql or "send whatsapp" in ql:
        speak("Please speak the full number including country code, like plus nine one ...")
        number = listen(timeout=8)
        speak("What message should I send?")
        msg = listen(timeout=12)
        if number and msg and number != "None" and msg != "None":
            whatsapp.send_whatsapp_pywhatkit(number, msg)

    # News
    elif "news" in ql:
        news.read_news()

    # Weather
    elif "weather" in ql:
        speak("Which city?")
        city = listen(timeout=6)
        if city and city != "None":
            weather.get_weather(city)

    # Jokes/Facts/Quotes
    elif "joke" in ql:
        jokes.tell_joke()
    elif "fact" in ql:
        jokes.tell_fact()
    elif "quote" in ql:
        jokes.tell_quote()

    # Volume / System control
    elif "volume up" in ql or "increase volume" in ql:
        system_control.set_volume(80)
    elif "volume down" in ql or "decrease volume" in ql:
        system_control.set_volume(30)
    elif "shutdown" in ql:
        system_control.shutdown_pc()
    elif "restart" in ql:
        system_control.restart_pc()
    elif "lock" in ql:
        system_control.lock_pc()

    # Exit
    elif any(x in ql for x in ("exit","quit","goodbye","stop")):
        speak("Shutting down. Goodbye.")
        break

    else:
        speak("Command not recognized. Should I search the web for that?")
        ans = listen(timeout=4)
        if ans and "yes" in ans.lower():
            import webbrowser
            webbrowser.open("https://www.google.com/search?q=" + ql)

    WAKE_EVENT.clear()
    time.sleep(0.2)
