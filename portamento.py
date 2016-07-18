from helpers import millisec_to_samples, interpolate_value


class Portamento():

    def __init__(self):
        self.old_pitch = None
        self.current_pitch = 220
        self.new_pitch = None
        self.t = 0.0
        self.value = 100.0
        self.nt_on = False

    def next_sample(self):
        if self.t > 0.0:
            self.current_pitch = interpolate_value(self.t, millisec_to_samples(self.value), self.new_pitch, self.old_pitch)
            self.t -= 1.0

        return self.current_pitch

    def note_on(self, pitch):
        if self.nt_on:
            self.t = millisec_to_samples(self.value)
            self.new_pitch = pitch
        else:
            self.current_pitch = pitch
            self.nt_on = True

        self.old_pitch = self.current_pitch

    def note_off(self):
        self.nt_on = False
