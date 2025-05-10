from time import sleep
import evdev

from src.hotkeys import hotkey

# If a hotkey returns True, it will block the event
@hotkey(r".*Text Editor", "t")
def notepad(ui, event):
    ui.write_string("Hello, Notepad!")
    return True
