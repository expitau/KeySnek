import { Extension, gettext as _ } from 'resource:///org/gnome/shell/extensions/extension.js';
import Gio from 'gi://Gio';

const DBUS_SCHEMA = `
<node>
    <interface name="org.gnome.shell.extensions.KeySnek">
        <method name="GetActiveWindow">
            <arg type="s" direction="out" name="windowTitle" />
        </method>
        <method name="SetActiveWindow">
            <arg type="s" direction="in" name="windowTitle" />
        </method>
        <method name="Eval">
            <arg type="s" direction="in" name="command" />
            <arg type="s" direction="out" name="result" />
        </method>
    </interface>
</node>`;

export default class KeySnekDbus extends Extension {
  GetActiveWindow() {
    return global.get_window_actors().find((window) =>
      window.meta_window.has_focus()
    ).meta_window.get_title();
  }

  SetActiveWindow(windowTitle) {
    global.get_window_actors().find((window) =>
      window.meta_window.get_title().match(windowTitle)
    ).meta_window.activate(global.get_current_time());
  }

  // Eval(command) {
  //   return eval(command);
  // }

  enable() {
    this._dbus = Gio.DBusExportedObject.wrapJSObject(DBUS_SCHEMA, this);
    this._dbus.export(
      Gio.DBus.session,
      "/org/gnome/shell/extensions/KeySnek"
    );
  }

  disable() {
    this._dbus.flush();
    this._dbus.unexport();
    delete this._dbus;
  }
}
