# features/system_control.py
import os, platform
from utils.speech import speak

def shutdown_pc():
    if platform.system() == 'Windows':
        speak("Shutting down")
        os.system("shutdown /s /t 5")
    else:
        speak("Shutdown not implemented for this OS")

def restart_pc():
    if platform.system() == 'Windows':
        speak("Restarting")
        os.system("shutdown /r /t 5")

def lock_pc():
    if platform.system() == 'Windows':
        import ctypes
        ctypes.windll.user32.LockWorkStation()

def set_volume(percent:int):
    """
    Attempt pycaw; fallback to keyboard presses (approx).
    """
    try:
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        from comtypes import CLSCTX_ALL
        from ctypes import cast, POINTER
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        minV, maxV = volume.GetVolumeRange()[:2]
        target = minV + (maxV - minV) * (percent / 100.0)
        volume.SetMasterVolumeLevel(target, None)
        speak(f"Volume set to {percent} percent")
    except Exception:
        import pyautogui
        if percent > 50:
            for _ in range((percent-50)//5):
                pyautogui.press("volumeup")
        else:
            for _ in range((50-percent)//5):
                pyautogui.press("volumedown")
        speak("Adjusted volume approximately")
