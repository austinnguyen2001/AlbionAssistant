from pynput import keyboard
from tkWindow import TkWindow
import wmi
import cv2

gui = TkWindow()
process_manager = wmi.WMI()
open_process_watcher = process_manager.Win32_Process.watch_for("Creation")
close_process_watcher = process_manager.Win32_Process.watch_for("Deletion")

def on_release(key):
    try: 
        if key.char == 'l': gui.toggle_visibility()
    except Exception: pass

listener = keyboard.Listener(on_release=on_release)

# Only run when Albion is open
while True:
    new_process = open_process_watcher()
    close_process = close_process_watcher()
    if new_process.Caption == "Albion-Online.exe":
        with listener:
            gui.start_loop()
            listener.join()
    
    if close_process.Caption == "Albion-Online.exe":
        gui.destroy()
        listener.stop()