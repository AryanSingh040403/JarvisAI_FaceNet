# features/notes.py
from pathlib import Path
import json, datetime
from config import NOTES_FILE

if not NOTES_FILE.exists():
    NOTES_FILE.write_text(json.dumps({'notes':[], 'todos':[]}, indent=2))

def add_note(text: str):
    d = json.loads(NOTES_FILE.read_text())
    d['notes'].append({'text': text, 'time': datetime.datetime.now().isoformat()})
    NOTES_FILE.write_text(json.dumps(d, indent=2))

def list_notes(n=5):
    d = json.loads(NOTES_FILE.read_text())
    return d.get('notes', [])[-n:]

def add_todo(text: str):
    d = json.loads(NOTES_FILE.read_text())
    d['todos'].append({'task': text, 'done': False, 'time': datetime.datetime.now().isoformat()})
    NOTES_FILE.write_text(json.dumps(d, indent=2))

def list_todos():
    d = json.loads(NOTES_FILE.read_text())
    return d.get('todos', [])
