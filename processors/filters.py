from .processor import Processor


class SmoothingFilter(Processor):

    def __init__(self, smoothing_factor=0.1):
        self.smoothing_factor = smoothing_factor
        self.prev_delta = 0.0
        self.prev_x = 0.0

    def process_next(self, x, smoothing_factor=1.0, **mod_params):
        pure_delta = (x - self.prev_x)
        smoothing_factor *= self.smoothing_factor
        delta = smoothing_factor*self.prev_delta + (1.0 - smoothing_factor)*pure_delta
        self.prev_delta = delta
        return self.prev_x + delta





