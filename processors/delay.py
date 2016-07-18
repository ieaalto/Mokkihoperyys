from helpers import millisec_to_samples
from .processor import Processor


class Delay(Processor):
    MAX_DELAY = 2000
    MAX_BUFFER_SIZE = int(millisec_to_samples(MAX_DELAY))

    def __init__(self, time=200, feedback= 0.5, level=0.5):
        super().__init__()
        self.feedback = feedback
        self.level = level
        self.time = time
        self.buffer_size = round(millisec_to_samples(self.time))
        self.buffer = [0.0 for i in range(0, Delay.MAX_BUFFER_SIZE)]
        self.t = 0

    def process_next(self, x, time=1.0, **mod_parameters):
        out = x + self.buffer[self.t]*self.level
        self.buffer[self.t] = x + (self.buffer[self.t]*self.level)*self.feedback

        self.buffer_size = round(millisec_to_samples(self.time * time))
        self.t = self.t + 1 if self.t < self.buffer_size else 0
        return out

