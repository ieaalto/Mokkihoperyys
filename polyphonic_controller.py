from helpers import pitch_from_key


class PolyphonicController:

    def __init__(self, voices):
        self.n_voices = len(voices)
        self.voices = voices
        self.last_voice = 0
        self.pitch_shift = 0
        self.voice_keys = {}

    def note_on(self, velocity, key):
        pitch = pitch_from_key(key + self.pitch_shift)
        i = self.last_voice + 1 if self.last_voice < self.n_voices -1  else 0
        self.last_voice = i

        self.voices[i].change_pitch(pitch)
        self.voices[i].note_on()
        self.voice_keys[key] = i


    def note_off(self, key):
        pitch = pitch_from_key(key + self.pitch_shift)
        i = self.voice_keys[key]

        self.voices[i].note_off()


