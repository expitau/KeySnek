import evdev

class UInput(evdev.UInput):
    def write_string(self, s):
        characters = {
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
        }
        uppercase = {
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
        }

        for c in s:
            if c in uppercase:
                self.write(evdev.ecodes.EV_KEY, evdev.ecodes.KEY_LEFTSHIFT, 1)
                self.write(evdev.ecodes.EV_KEY, uppercase[c], 1)
                self.write(evdev.ecodes.EV_KEY, uppercase[c], 0)
                self.write(evdev.ecodes.EV_KEY, evdev.ecodes.KEY_LEFTSHIFT, 0)
            elif c in characters:
                self.write(evdev.ecodes.EV_KEY, characters[c], 1)
                self.write(evdev.ecodes.EV_KEY, characters[c], 0)
            else:
                print(f"Unknown character: {c}")
                continue
        self.syn()
