# utils/app_launcher.py
import json, os
from pathlib import Path
from utils.speech import speak
from config import APPS_FILE

def load_apps():
    if APPS_FILE.exists():
        try:
            return json.loads(APPS_FILE.read_text())
        except Exception:
            return {}
    else:
        default = {
            "vscode": os.path.expandvars(r"%LOCALAPPDATA%\\Programs\\Microsoft VS Code\\Code.exe"),
            "chrome": r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        }
        APPS_FILE.write_text(json.dumps(default, indent=2))
        return default

def open_app(name: str) -> bool:
    name = name.lower().strip()
    apps = load_apps()
    if name in apps:
        path = os.path.expandvars(apps[name])
        path = os.path.expanduser(path)
        if Path(path).exists():
            os.startfile(path)
            speak(f"Opening {name}")
            return True
        else:
            speak(f"Configured path not found: {path}")
            return False
    # fuzzy match
    for k, v in apps.items():
        if name in k:
            p = os.path.expandvars(v)
            if Path(p).exists():
                os.startfile(p)
                speak(f"Opening {k}")
                return True
    speak(f"{name} not configured in apps.json")
    return False
