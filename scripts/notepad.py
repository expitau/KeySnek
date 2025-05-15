from time import sleep
import evdev
from src.hotkeys import hotkey, hotkey_raw, event_matches

# Run our notepad function if SHIFT-T is pressed in a window matching ".*Text Editor"
# If a hotkey returns True, it will block the event
@hotkey(r".*Text Editor", "+t")
def notepad(ui, event, device):
    ui.write_string("Hello, Notepad!")
    return True

event_log = []
recording = False
@hotkey_raw(r".*")
def record(ui, event, device):
    global event_log, recording
    if event.type == evdev.ecodes.EV_KEY and event.code == evdev.ecodes.KEY_R and event.value == 1 and evdev.ecodes.KEY_LEFTMETA in device.active_keys() and evdev.ecodes.KEY_LEFTSHIFT in device.active_keys():
        if recording:
            recording = False
            print("Recording stopped")
            for i in range(1):
                last_timestamp = min([e.timestamp() for e in event_log])
                for event in event_log:
                    sleep(event.timestamp() - last_timestamp)
                    if (event.type != evdev.ecodes.EV_SYN):
                        print("Replaying", evdev.categorize(event))
                    ui.write_event(event)
                    last_timestamp = event.timestamp()
                    # print(event.timestamp() - initial_timestamp, f"ui.write({event.type}, {event.code}, {event.value})")
            ui.write(evdev.ecodes.EV_KEY, evdev.ecodes.KEY_LEFTMETA, 0)
            ui.write(evdev.ecodes.EV_KEY, evdev.ecodes.KEY_LEFTSHIFT, 0)
            ui.syn()
        else:
            recording = True
            event_log = []
            print("Recording started")
        return True
    if recording:
        event_log.append(event)
    # print(device.name, evdev.categorize(event))
