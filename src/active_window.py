import asyncio
import os
import re

active_hotkeys = []
registered_hotkeys = []

window_name = None
def get():
    return window_name

def hotkeys():
    return active_hotkeys

gdbus_regex = re.compile(r'^\s*\(\'(.*)\',\)\s*$')
def update():
    global window_name
    result = os.popen("gdbus call --address=unix:path=/run/user/1000/bus --dest org.gnome.Shell --object-path /org/gnome/shell/extensions/KeySnek --method org.gnome.shell.extensions.KeySnek.GetActiveWindow").read().strip()

    match = re.search(gdbus_regex, result)

    if not match:
        return None

    window_name = match.group(1)
