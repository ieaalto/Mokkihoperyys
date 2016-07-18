from helpers import pitch_from_key
from portamento import Portamento


class MonophonicController:

    def __init__(self, note_on_callback, note_off_callback):
        self.note_on_callback = note_on_callback
        self.note_off_callback = note_off_callback

        self.portamento = Portamento()
        self.volume = 0.8
        self.keys_pressed = []
        self.pitch_shift = 0.0

    def next_pitch(self):
        return self.portamento.next_sample()

    def note_on(self, velocity, key):
        pitch = pitch_from_key(key + self.pitch_shift)
        any_pressed = self.any_key_pressed()
        self.press_key(pitch)

        self.portamento.note_on(pitch)
        if not any_pressed:
            self.note_on_callback()

    def note_off(self, key):
        pitch = pitch_from_key(key + self.pitch_shift)
        self.release_key(pitch)

        if self.any_key_pressed():
            new_pitch = self.keys_pressed[-1]
            self.portamento.note_on(new_pitch)
        else:
            self.note_off_callback()
            self.portamento.note_off()

    def press_key(self, pitch):
        self.keys_pressed.append(pitch)

    def release_key(self, pitch):
        i = self.keys_pressed.index(pitch)
        self.keys_pressed.pop(i)

    def any_key_pressed(self):
        return True if len(self.keys_pressed) > 0 else False
