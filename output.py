import math
from settings import SAMPLE_RATE, SAMPLE_WIDTH, BUFFER_SIZE
import _thread


class Output:

    def __init__(self, mixer):
        self.mixer = mixer

    def get_chunk(self, chunk_size):
        data = b''
        max_val = int(pow(2, (SAMPLE_WIDTH * 8 - 1))) - 1

        for i in range(0, chunk_size):
            sample = round(self.mixer.next_sample() * max_val)
            data += sample.to_bytes(SAMPLE_WIDTH, byteorder='little', signed=True)

        return data





