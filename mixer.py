from helpers import clip
from monophonic_controller import MonophonicController
from oscillators import Oscillator, MultiOsc
from polyphonic_controller import PolyphonicController
from processors import Amp, Delay, LFO, Envelope


class Pipeline:

    def __init__(self, oscillators, processors):
        self.oscillators = oscillators
        self.processors = processors

    def note_on(self):
        for p in self.processors:
            p.note_on()

    def note_off(self):
        for p in self.processors:
            p.note_off()

    def change_pitch(self, pitch):
        for osc in self.oscillators:
            osc.change_pitch(pitch)

    def next_sample(self):
        out = 0.0

        for osc in self.oscillators:
            out += osc.next_sample()

        for p in self.processors:
            out = p.process_next(out)

        return clip(out, -1.0, 1.0)


class MonoMixer:

    def __init__(self, pipeline, controller=MonophonicController):
        self.pipeline = pipeline
        self.controller = controller(*_get_trigger_callbacks(self.pipeline))

    def next_sample(self):
        self.pipeline.change_pitch(self.controller.next_pitch())
        return self.pipeline.next_sample()

    def set_waveform(self, waveform):
        self.pipeline.oscillators[0].set_waveform(waveform)


class PolyMixer:

    def __init__(self, controller=PolyphonicController, voices=3):
        self.voices = voices
        self.pipelines = [Pipeline([Oscillator(waveform_index=3)],
                                   [Amp(gain=0.3)]) for i in range(0, self.voices)]
        self.controller = controller(self.pipelines)

    def next_sample(self):
        out = 0.0
        for pline in self.pipelines:
            out += pline.next_sample()
        return clip(out, -1.0, 1.0)

    def set_waveform(self, waveform):
        for p in self.pipelines:
            p.oscillators[0].set_waveform(waveform)


def _get_trigger_callbacks(pipeline):

    def note_on():
        pipeline.note_on()

    def note_off():
        pipeline.note_off()

    return note_on, note_off