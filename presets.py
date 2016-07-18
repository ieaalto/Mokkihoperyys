from mixer import Pipeline
from oscillators import Oscillator, MultiOsc
from processors import Amp, Delay, Envelope, LFO, SmoothingFilter
from processors.prefabs import AmpEnvelope


SIMPLE = Pipeline([Oscillator(waveform_index=1)], [AmpEnvelope(gain=0.9, attack=200, decay=400, sustain=0.7, release=25)])

TREMOLO = Pipeline([Oscillator(waveform_index=1)], [Envelope(LFO(Amp(gain=0.7),
                                                                 ['gain'], freq=5, amount=0.25), ['gain'],
                                                             attack=125, decay=200, sustain=0.7, release=20)])

ENVELOPED_TREMOLO = Pipeline([Oscillator(waveform_index=0)], [Envelope(LFO(Amp(gain=0.7),
                                                                 ['gain'], freq=10, amount=0.2), ['gain', 'pitch'],
                                                             attack=125, decay=500, sustain=0.2, release=20)])

DELAYED = Pipeline([Oscillator(waveform_index=1)], [AmpEnvelope(gain=0.6),
                                                    Delay(time=150, feedback=0.8, level=0.6)])

MULTIOSC = Pipeline([MultiOsc([Oscillator(waveform_index=0),
                               Oscillator(waveform_index=0, pitch_shift=3),
                               Oscillator(waveform_index=0, pitch_shift=7),
                               Oscillator(waveform_index=0, pitch_shift=12)])], [AmpEnvelope(gain=0.7),
                                                                                 SmoothingFilter(smoothing_factor=0.5)])

TWO_OSCILLATORS = Pipeline([Oscillator(waveform_index=1), Oscillator(waveform_index=0, pitch_shift=7, volume=0.7)],
                           [AmpEnvelope(gain=0.4), Delay()])

RESONANCE = Pipeline([MultiOsc([Oscillator(waveform_index=1),
                                Oscillator(waveform_index=1, volume=0.5, pitch_mul=2),
                                Oscillator(waveform_index=1, volume=0.3, pitch_mul=3)
                                ])],
                     [AmpEnvelope(gain=0.3, attack=600),
                      Delay(time=20, feedback=0.999, level=0.9)]
                     )

SMOOTH = Pipeline([Oscillator(waveform_index=2)], [AmpEnvelope(gain=0.9, attack=200, decay=400, sustain=0.7, release=25),
                                                   SmoothingFilter(smoothing_factor=0.98),
                                                   Delay(time=150, feedback=0.95, level=0.4)])