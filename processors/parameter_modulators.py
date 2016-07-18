from helpers import millisec_to_samples, interpolate_value
from oscillators.oscillator import Oscillator
from .processor import Processor


class ParameterModulator(Processor):

    def __init__(self, processor, parameters):
        super().__init__()
        self.processor = processor
        self.parameters = parameters

    def note_on(self):
        self._note_on()
        self.processor.note_on()

    def note_off(self):
        self._note_off()
        self.processor.note_off()

    def _note_on(self):
        pass

    def _note_off(self):
        pass

    def next_sample(self, **mod_parameters):
        raise NotImplementedError

    def process_next(self, x, **mod_parameters):
        mod = self.next_sample(**mod_parameters)
        for param in self.parameters:
            mod_parameters[param] = mod_parameters[param]*mod if param in mod_parameters else mod

        return self.processor.process_next(x, **mod_parameters)


class LFO(ParameterModulator):

    def __init__(self, processor, parameters, freq= 5, amount=0.1, waveform=Oscillator.SINE):
        super().__init__(processor, parameters)
        self.oscillator = Oscillator(waveform_index=waveform)
        self.oscillator.change_pitch(freq)
        self.amount = amount
        self.freq = freq

    def next_sample(self, amount=1.0, pitch=1.0, **mod_params):
        self.oscillator.change_pitch(self.freq * pitch)
        return 1.0 + self.oscillator.next_sample() * (self.amount * amount)


class Envelope(ParameterModulator):
    _OFF = 0
    _ATTACK = 1
    _DECAY = 2
    _SUSTAIN = 3
    _RELEASE = 4

    def __init__(self, processor, parameters, attack=50, decay=400, sustain=0.8, release=25):
        super().__init__(processor, parameters)
        self.state = Envelope._OFF
        self.attack = attack
        self.decay = decay
        self.sustain = sustain
        self.release = release
        self.t = 0.0
        self.value = 0.0
        self.mem = 0.0

    def next_sample(self, **mod_parameters):
        if self.state == Envelope._OFF:
            self.value = 0.0
        elif self.state == Envelope._ATTACK:
            if self.t >= millisec_to_samples(self.attack):
                self.state = Envelope._DECAY
                self.t = millisec_to_samples(self.decay)
                self.value = 1.0
            else:
                self.t += 1.0
                self.value = interpolate_value(self.t, millisec_to_samples(self.attack), self.mem, 1.0)

        elif self.state == Envelope._DECAY:
            if self.t <= 0.0:
                self.state = Envelope._SUSTAIN
                self.t = 0.0
                self.value = self.sustain
            else:
                self.t -= 1.0
                self.value = interpolate_value(self.t, millisec_to_samples(self.decay), self.sustain, 1.0)

        elif self.state == Envelope._SUSTAIN:
            self.value = self.sustain

        else:
            if self.t <= 0.0:
                self.state = Envelope._OFF
                self.value = 0.0
            else:
                self.t -= 1.0
                self.value = interpolate_value(self.t, millisec_to_samples(self.release), 0.0, self.mem)

        return self.value

    def _note_on(self):
        self.state = Envelope._ATTACK
        self.t = 0.0
        self.mem = self.value

    def _note_off(self):
        if self.state != Envelope._OFF:
            self.mem = self.value
            self.state = Envelope._RELEASE
            self.t = millisec_to_samples(self.release)

