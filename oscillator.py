import math


class Oscillator:

    def __init__(self, sample_rate, sample_width):
        self.sample_rate = sample_rate
        self.sample_width = sample_width
        self.pitch = 440
        self.nt_on = True
        self.samples_per_period = self.sample_rate / self.pitch
        self.t = 0

    def set_pitch(self, pitch):
        self.pitch = pitch
        self.samples_per_period = self.sample_rate / self.pitch

    def note_on(self):
        self.nt_on = True

    def note_off(self):
        self.nt_on = False

    def sine(self, x, norm):
        return math.sin(((x / norm) * 2 * math.pi))

    def tri(self, x, norm):
        return (x / norm)*2 - 1

    def square(self, x , norm):
        val = -1 if x <= norm/2 else 1
        return val

    def get_audio(self, chunk_size, waveform):
        data = b''

        for i in range(0, chunk_size):
            sample = self._get_next_sample(waveform) if self.nt_on else 0
            data += sample.to_bytes(self.sample_width, byteorder='little', signed=True)

        return data

    def _get_next_sample(self, waveform):
        max_val = int(pow(2, (self.sample_width * 8)) / 2) - 1
        sample = round(waveform(self.t, self.samples_per_period) * max_val)

        self.t = self.t + 1 if self.t < self.samples_per_period - 1 else 0
        return sample
