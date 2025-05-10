# KeySnek

KeySnek is a hotkey daemon for Linux that works seamlessly with Wayland and Gnome

## Installation

### Step 1 - Give root permission to access session dbus
Create a new file in `/etc/dbus-1/session-local.conf`, and add the following to it
```xml
<busconfig>
  <policy context="mandatory">
    <allow user="root"/>
  </policy>
</busconfig>
```

### Step 2 - Install the gnome extension to allow reading of active window
Run
```sh
gnome-extensions pack extension --force
gnome-extensions install keysnek\@expitau.shell-extension.zip
gnome-extensions enable keysnek\@expitau
```

### Step 3 - Install dependencies
```
python -m venv .venv
.venv/bin/pip install evdev
```

### Step 4 - Run the script as root
```
sudo .venv/bin/python main.py
```

## Usage
See example in [notepad.py](./scripts/notepad.py)

```py

# Run our notepad function if "t" is pressed in a window matching ".*Text Editor"
# If a hotkey returns True, it will block the event
@hotkey(r".*Text Editor", "t")
def notepad(ui, event):
    ui.write_string("Hello, Notepad!")
    return True
```
