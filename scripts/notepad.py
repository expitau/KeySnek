from time import sleep

from src.hotkeys import hotkey

# Run our notepad function if SHIFT-T is pressed in a window matching ".*Text Editor"
# If a hotkey returns True, it will block the event
@hotkey(r".*Text Editor", "+t")
def notepad(ui, event, all_keys):
    ui.write_string("Hello, Notepad!")
    return True
