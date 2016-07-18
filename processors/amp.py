from .processor import Processor


class Amp(Processor):

    def __init__(self, gain=1.0):
        super().__init__()
        self.gain = gain

    def process_next(self,x, gain=1.0, **mod_parameters):
        return x * self.gain * gain
