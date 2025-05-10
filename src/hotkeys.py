import re
import evdev

from src import keymap

registered_hotkeys = []

def get_registered_hotkeys():
    return registered_hotkeys

def _event_matches(event, hotkey):
    if event.type == evdev.ecodes.EV_KEY and event.value != 0:
        if event.code in [keymap.CHARACTERS.get(c) for c in hotkey]:
            return True
    return False


def hotkey(window_context: str, hotkey: str):
    window_regex = re.compile(window_context)
    def decorator(func):
        def wrapper(ui, event, *args, **kwargs):
            try:
                if not _event_matches(event, hotkey):
                    return None
                return func(ui, event, *args, **kwargs)
            except Exception as e:
                print(f"Error in hotkey '{func.__name__}': {e}")
                return None
        registered_hotkeys.append([window_regex, wrapper])
        return wrapper
    return decorator

def hotkey_raw(window_context: str):
    window_regex = re.compile(window_context)
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                print(f"Error in hotkey '{func.__name__}': {args}, {kwargs}")
                return None
        registered_hotkeys.append([window_regex, wrapper])
        return wrapper
    return decorator
