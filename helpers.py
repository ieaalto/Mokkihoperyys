from settings import SAMPLE_RATE
import math


def millisec_to_samples(ms):
    return ms * (SAMPLE_RATE / 1000)


def pitch_from_key(key):
    return 220 * math.pow(2, key/12)


def interpolate_value(t, param, start_value, end_value):
        if start_value > end_value:
            t = abs(t - param)

        quot = t / param

        min_val = min(start_value, end_value)
        max_val = max(start_value, end_value)

        return (quot * max_val) - (quot * min_val) + min_val

def clip(x, min, max):
    if x < min: x = -1.0
    if x > max: x = 1.0
    return x