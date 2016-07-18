from oscillators import Oscillator


class MultiOsc:

    def __init__(self, oscillators = None):
        self.oscillators = oscillators if oscillators else []
        self.last_values = [0.0] * len(self.oscillators)
        self.last_values_sum = 0.0
        self.t = 0

    def add_voice(self, waveform_index=0, pitch_shift=0.0, pitch_mul=1.0, volume=1.0):
        self.oscillators.append(Oscillator(waveform_index=waveform_index, pitch_shift=pitch_shift,
                                           pitch_mul=pitch_mul, volume=volume))
        self.last_values.append(0.0)

    def change_pitch(self, pitch):
        for osc in self.oscillators:
            osc.change_pitch(pitch)

    def next_sample(self):
        new_sample = self.oscillators[self.t].next_sample(dt=len(self.oscillators))
        self.last_values_sum -= self.last_values[self.t]
        sample = new_sample + self.last_values_sum

        self.last_values_sum += new_sample
        self.last_values[self.t] = new_sample

        self.t = (self.t + 1)%len(self.oscillators)
        return sample
