import re
import evdev

from src import keymap

registered_hotkeys = []

def get_registered_hotkeys():
    return registered_hotkeys

def _event_matches(event, all_keys, hotkey):
    key_set = set(all_keys)

    if event.type != evdev.ecodes.EV_KEY:
        return False
    
    if event.value == evdev.KeyEvent.key_up:
        return False

    for c in hotkey:
        # If requesting a shift
        if c == "+":
            # And we did not press a shift
            if not (evdev.ecodes.KEY_LEFTSHIFT in key_set or evdev.ecodes.KEY_RIGHTSHIFT in key_set):
                return False
            # Otherwise remove shift from list of pressed keys
            key_set = key_set - {evdev.ecodes.KEY_LEFTSHIFT, evdev.ecodes.KEY_RIGHTSHIFT}
        elif c == "^":
            if not (evdev.ecodes.KEY_LEFTCTRL in key_set or evdev.ecodes.KEY_RIGHTCTRL in key_set):
                return False
            key_set = key_set - {evdev.ecodes.KEY_LEFTCTRL, evdev.ecodes.KEY_RIGHTCTRL}
        elif c == "!":
            if not (evdev.ecodes.KEY_LEFTALT in key_set or evdev.ecodes.KEY_RIGHTALT in key_set):
                return False
            key_set = key_set - {evdev.ecodes.KEY_LEFTALT, evdev.ecodes.KEY_RIGHTALT}
        elif c == "#":
            if not (evdev.ecodes.KEY_LEFTMETA in key_set or evdev.ecodes.KEY_RIGHTMETA in key_set):
                return False
            key_set = key_set - {evdev.ecodes.KEY_LEFTMETA, evdev.ecodes.KEY_RIGHTMETA}
        elif c != "~" and c != "*":
            if keymap.CHARACTERS[c.lower()] not in key_set:
                return False
            key_set = key_set - {keymap.CHARACTERS[c.lower()]}
    
    # If there were any keys that were pressed, but not requested, and we don't have a *
    if len(key_set) > 0 and "*" not in hotkey:
        return False
    
    return True

def hotkey(window_context: str, hotkey: str):
    window_regex = re.compile(window_context)
    def decorator(func):
        def wrapper(ui, event, all_keys, *args, **kwargs):
            try:
                if not _event_matches(event, all_keys, hotkey):
                    return None
                result = func(ui, event, all_keys, *args, **kwargs)
                if "~" in hotkey:
                    return False
                return result
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
