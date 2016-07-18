import math
from matplotlib import pyplot as plt
from settings import SAMPLE_RATE


def sine(x):
    x += 1.0
    return math.sin((x * math.pi))


def saw(x):
    return x


def square(x):
    return -1.0 if x < 0.0 else 1.0


def tri(x):
    x += 1
    x *= 2
    x = x if x <= 1.0 else 1 - (x-1)
    x = x if x >= -1.0 else -1.0 + (abs(x) - 1)
    return x


class Oscillator:
    SINE = 0
    TRI = 1
    SQUARE = 2
    SAW = 3
    _WFS = [sine, tri, square, saw]

    def __init__(self, waveform_index=0, pitch_shift=0.0, pitch_mul=1.0, volume=1.0):
        self.pitch = 440
        self.samples_per_period = SAMPLE_RATE / self.pitch
        self.t = -(self.samples_per_period / 2)
        self.wf_index = waveform_index
        self.set_waveform(self.wf_index)
        self.pitch_mem = 440
        self.nt_on = False
        self.pitch_shift = pitch_shift
        self.pitch_mul = pitch_mul
        self.volume = volume

    def _set_pitch(self, pitch):
        self.pitch = pitch
        self.samples_per_period = SAMPLE_RATE / self.pitch
        self.t = -(self.samples_per_period / 2)

    def change_pitch(self, pitch):
        self.pitch_mem = max(pitch * math.pow(2, self.pitch_shift / 12) * self.pitch_mul, 1.0)

    def set_waveform(self, waveform_index):
        self.wf_index = waveform_index
        self.waveform = Oscillator._WFS[self.wf_index]

    def toggle_waveform(self):
        self.set_waveform(self.wf_index + 1 if self.wf_index < len(Oscillator._WFS) - 1 else 0)

    def next_sample(self, dt=1.0):
        if self.t < (self.samples_per_period / 2) - (dt-1):
            self.t += dt
        else:
            if self.pitch_mem != self.pitch:
                self._set_pitch(self.pitch_mem)
            else:
                self.t -= self.samples_per_period

        sample = self.waveform((self.t / (self.samples_per_period / 2)))
        return sample*self.volume

    def plot(self, n):
        arr = []

        for i in range(0, n):
            arr.append(self.next_sample())

        plt.plot(arr)
        plt.draw()
        plt.show()


