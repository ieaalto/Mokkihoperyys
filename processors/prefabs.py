from .parameter_modulators import Envelope
from .amp import Amp


def AmpEnvelope(gain=1.0, attack=100, decay=300, sustain=0.8, release=25):
    return Envelope(Amp(gain), ['gain'], attack=attack, decay=decay, sustain=sustain, release=release)
