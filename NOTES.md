To allow user to modify uinput (no longer necessary, see below)
- Write `KERNEL=="event*", SUBSYSTEM=="input", GROUP="input", MODE="660"` to `/etc/udev/rules.d/99-input.rules` (new file)
- Add nathan to group `input`

To allow root to access user dbus, write
```
<busconfig>
  <policy context="mandatory">
    <allow user="root"/>
  </policy>
</busconfig>
```
to `/etc/dbus-1/session-local.conf` (new file)

Then you can use `gdbus call --address=unix:path=/run/user/1000/bus --dest org.gnome.Shell --object-path /org/gnome/shell/extensions/KeySnek --method org.gnome.shell.extensions.KeySnek.GetActiveWindow` from root
