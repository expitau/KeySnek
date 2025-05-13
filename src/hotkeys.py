import re
import evdev
import traceback

registered_hotkeys = []

def get_registered_hotkeys():
    return registered_hotkeys

CHARACTERS = {
    'a': evdev.ecodes.KEY_A,
    'b': evdev.ecodes.KEY_B,
    'c': evdev.ecodes.KEY_C,
    'd': evdev.ecodes.KEY_D,
    'e': evdev.ecodes.KEY_E,
    'f': evdev.ecodes.KEY_F,
    'g': evdev.ecodes.KEY_G,
    'h': evdev.ecodes.KEY_H,
    'i': evdev.ecodes.KEY_I,
    'j': evdev.ecodes.KEY_J,
    'k': evdev.ecodes.KEY_K,
    'l': evdev.ecodes.KEY_L,
    'm': evdev.ecodes.KEY_M,
    'n': evdev.ecodes.KEY_N,
    'o': evdev.ecodes.KEY_O,
    'p': evdev.ecodes.KEY_P,
    'q': evdev.ecodes.KEY_Q,
    'r': evdev.ecodes.KEY_R,
    's': evdev.ecodes.KEY_S,
    't': evdev.ecodes.KEY_T,
    'u': evdev.ecodes.KEY_U,
    'v': evdev.ecodes.KEY_V,
    'w': evdev.ecodes.KEY_W,
    'x': evdev.ecodes.KEY_X,
    'y': evdev.ecodes.KEY_Y,
    'z': evdev.ecodes.KEY_Z,
    '0': evdev.ecodes.KEY_0,
    '1': evdev.ecodes.KEY_1,
    '2': evdev.ecodes.KEY_2,
    '3': evdev.ecodes.KEY_3,
    '4': evdev.ecodes.KEY_4,
    '5': evdev.ecodes.KEY_5,
    '6': evdev.ecodes.KEY_6,
    '7': evdev.ecodes.KEY_7,
    '8': evdev.ecodes.KEY_8,
    '9': evdev.ecodes.KEY_9,
    ' ': evdev.ecodes.KEY_SPACE,
    '\n': evdev.ecodes.KEY_ENTER,
    '\'': evdev.ecodes.KEY_APOSTROPHE,
    '`': evdev.ecodes.KEY_GRAVE,
    ',': evdev.ecodes.KEY_COMMA,
    '.': evdev.ecodes.KEY_DOT,
    ';': evdev.ecodes.KEY_SEMICOLON,
    '-': evdev.ecodes.KEY_MINUS,
    '=': evdev.ecodes.KEY_EQUAL,
    '[': evdev.ecodes.KEY_LEFTBRACE,
    ']': evdev.ecodes.KEY_RIGHTBRACE,
    '\\': evdev.ecodes.KEY_BACKSLASH,
    '/': evdev.ecodes.KEY_SLASH,
}
SHIFT_CHARACTERS = {
    'A': evdev.ecodes.KEY_A,
    'B': evdev.ecodes.KEY_B,
    'C': evdev.ecodes.KEY_C,
    'D': evdev.ecodes.KEY_D,
    'E': evdev.ecodes.KEY_E,
    'F': evdev.ecodes.KEY_F,
    'G': evdev.ecodes.KEY_G,
    'H': evdev.ecodes.KEY_H,
    'I': evdev.ecodes.KEY_I,
    'J': evdev.ecodes.KEY_J,
    'K': evdev.ecodes.KEY_K,
    'L': evdev.ecodes.KEY_L,
    'M': evdev.ecodes.KEY_M,
    'N': evdev.ecodes.KEY_N,
    'O': evdev.ecodes.KEY_O,
    'P': evdev.ecodes.KEY_P,
    'Q': evdev.ecodes.KEY_Q,
    'R': evdev.ecodes.KEY_R,
    'S': evdev.ecodes.KEY_S,
    'T': evdev.ecodes.KEY_T,
    'U': evdev.ecodes.KEY_U,
    'V': evdev.ecodes.KEY_V,
    'W': evdev.ecodes.KEY_W,
    'X': evdev.ecodes.KEY_X,
    'Y': evdev.ecodes.KEY_Y,
    'Z': evdev.ecodes.KEY_Z,
    '!': evdev.ecodes.KEY_1,
    '@': evdev.ecodes.KEY_2,
    '#': evdev.ecodes.KEY_3,
    '$': evdev.ecodes.KEY_4,
    '%': evdev.ecodes.KEY_5,
    '^': evdev.ecodes.KEY_6,
    '&': evdev.ecodes.KEY_7,
    '*': evdev.ecodes.KEY_8,
    '(': evdev.ecodes.KEY_9,
    ')': evdev.ecodes.KEY_0,
    '_': evdev.ecodes.KEY_MINUS,
    '+': evdev.ecodes.KEY_EQUAL,
    '{': evdev.ecodes.KEY_LEFTBRACE,
    '}': evdev.ecodes.KEY_RIGHTBRACE,
    '|': evdev.ecodes.KEY_BACKSLASH,
    ':': evdev.ecodes.KEY_SEMICOLON,
    '"': evdev.ecodes.KEY_APOSTROPHE,
    '<': evdev.ecodes.KEY_COMMA,
    '>': evdev.ecodes.KEY_DOT,
    '?': evdev.ecodes.KEY_SLASH,
    '~': evdev.ecodes.KEY_GRAVE,
}

def event_matches(event, all_keys, hotkey):
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
            if c in CHARACTERS:
                if CHARACTERS[c] not in key_set:
                    return False
                key_set = key_set - {CHARACTERS[c]}
            
            if c in SHIFT_CHARACTERS:
                if SHIFT_CHARACTERS[c] not in key_set:
                    return False
                key_set = key_set - {SHIFT_CHARACTERS[c]}
            
    # If there were any keys that were pressed, but not requested, and we don't have a *
    if len(key_set) > 0 and "*" not in hotkey:
        return False
    
    return True

def hotkey(window_context: str, hotkey: str):
    window_regex = re.compile(window_context)
    def decorator(func):
        def wrapper(ui, event, device, *args, **kwargs):
            try:
                if not event_matches(event, device.active_keys(), hotkey):
                    return None
                result = func(ui, event, device, *args, **kwargs)
                if "~" in hotkey:
                    return False
                return result
            except Exception:
                print(f"Error in hotkey '{func.__name__}': {args}, {kwargs}")
                print(traceback.format_exc())
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
            except Exception:
                print(f"Error in hotkey '{func.__name__}': {args}, {kwargs}")
                print(traceback.format_exc())
                return None
        registered_hotkeys.append([window_regex, wrapper])
        return wrapper
    return decorator
