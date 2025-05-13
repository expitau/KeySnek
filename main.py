import re
import evdev
from select import select
from time import sleep
import asyncio

from scripts import notepad

from src import active_window
from src.uinput import UInput
from src.hotkeys import get_registered_hotkeys

from src import failsafe
failsafe.set_failsafe(40)

active_hotkeys = []

async def handle_events(ui: UInput, device: evdev.InputDevice):
    async for event in device.async_read_loop():
        # print(device.name, evdev.categorize(event))
        blocked = False
        for hotkey in active_hotkeys:
            blocked = blocked or hotkey(ui, event, device)
        if not blocked:
            ui.write_event(event)

async def update():
    global active_hotkeys

    while True:
        await asyncio.sleep(1)

        # Update the active window name
        active_window.update()
        result = active_window.get()
        if result is None:
            result = ''

        # Find which sets of hotkeys are active
        active_hotkeys = [x[1] for x in get_registered_hotkeys() if re.match(x[0], result)]

def main():
    devicePaths = ['/dev/input/event3', '/dev/input/event18']
    # devicePaths = ['/dev/input/event3']
    devices = [evdev.InputDevice(path) for path in devicePaths]
    for device in devices:
        device.grab()
        print(f"Device {device.path} registered: {device.name}")
    
    ui = UInput.from_device(*devices)

    main_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(main_loop)
    for device in devices:
        asyncio.ensure_future(handle_events(ui, device))

    asyncio.ensure_future(update())
    main_loop.run_forever()

if __name__ == "__main__":
    sleep(0.5)
    main()
