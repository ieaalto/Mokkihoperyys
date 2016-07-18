from helpers import pitch_from_key


_KEYS = {"n": -3, "m": -1, "a": 0, "w": 1, "s": 2, "e": 3, "d": 4, "f": 5, "t": 6, "g": 7, "y": 8, "h": 9, "u": 10, "j": 11,
         "k": 12, "o": 13, "l": 14}


def get_note_on_callback(mixer):

    def callback(event):
        if event.char in _KEYS:
            pitch = _KEYS[event.char]
            mixer.note_on(1, pitch)

    return callback


def get_note_off_callback(mixer):

    def callback(event):
        if event.char in _KEYS:
            pitch = _KEYS[event.char]
            mixer.note_off(pitch)

    return callback

def get_pitch_shifter(mixer, shift):
    def callback(event):
        mixer.pitch_shift += shift

    return callback

def map_keys(root, mixer):
    root.bind_all("<KeyPress>", get_note_on_callback(mixer))
    root.bind_all("<KeyRelease>", get_note_off_callback(mixer))
    root.bind_all("z", get_pitch_shifter(mixer, -1))
    root.bind_all("x", get_pitch_shifter(mixer, +1))