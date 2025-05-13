import evdev

hex_to_key = {
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
    'A': evdev.ecodes.KEY_A,
    'B': evdev.ecodes.KEY_B,
    'C': evdev.ecodes.KEY_C,
    'D': evdev.ecodes.KEY_D,
    'E': evdev.ecodes.KEY_E,
    'F': evdev.ecodes.KEY_F,
}

class UInput(evdev.UInput):
    def write_char(self, c):
        self.write(evdev.ecodes.EV_KEY, evdev.ecodes.KEY_LEFTCTRL, 1)
        self.write(evdev.ecodes.EV_KEY, evdev.ecodes.KEY_LEFTSHIFT, 1)

        self.write(evdev.ecodes.EV_KEY, evdev.ecodes.KEY_U, 1)
        self.write(evdev.ecodes.EV_KEY, evdev.ecodes.KEY_U, 0)
        for h in "%X" % ord(c):
            self.write(evdev.ecodes.EV_KEY, hex_to_key[h], 1)
            self.write(evdev.ecodes.EV_KEY, hex_to_key[h], 0)
        
        self.write(evdev.ecodes.EV_KEY, evdev.ecodes.KEY_LEFTSHIFT, 0)
        self.write(evdev.ecodes.EV_KEY, evdev.ecodes.KEY_LEFTCTRL, 0)
        self.syn()
    
    def write_string(self, s):
        self.write(evdev.ecodes.EV_KEY, evdev.ecodes.KEY_LEFTCTRL, 1)
        self.write(evdev.ecodes.EV_KEY, evdev.ecodes.KEY_LEFTSHIFT, 1)

        for c in s:
            self.write(evdev.ecodes.EV_KEY, evdev.ecodes.KEY_U, 1)
            self.write(evdev.ecodes.EV_KEY, evdev.ecodes.KEY_U, 0)
            for h in "%X" % ord(c):
                self.write(evdev.ecodes.EV_KEY, hex_to_key[h], 1)
                self.write(evdev.ecodes.EV_KEY, hex_to_key[h], 0)
        
        self.write(evdev.ecodes.EV_KEY, evdev.ecodes.KEY_LEFTSHIFT, 0)
        self.write(evdev.ecodes.EV_KEY, evdev.ecodes.KEY_LEFTCTRL, 0)
        self.syn()
