import pyaudio
import wave
import time
from settings import SAMPLE_RATE, SAMPLE_WIDTH
from oscillator import Oscillator

p = pyaudio.PyAudio()
osc = Oscillator(SAMPLE_RATE, SAMPLE_WIDTH)
waveform = osc.square

#file = wave.open('output.wav', 'wb')
#file.setframerate(SAMPLE_RATE)
#file.setsampwidth(SAMPLE_WIDTH)
#file.setnchannels(2)


def callback(input_data, frame_count, time_info, status):
    data = osc.get_audio(frame_count, waveform)
    return data, pyaudio.paContinue

stream = p.open(format=p.get_format_from_width(SAMPLE_WIDTH),
                channels=1,
                rate=SAMPLE_RATE,
                output=True,
                stream_callback=callback
                )

stream.start_stream()

#data = osc.get_audio(CHUNK, waveform)

#for t in range(0, 1000):
#    stream.write(data)
#    file.writeframes(data)
#    data = osc.get_audio(CHUNK, waveform)

while stream.is_active():
    time.sleep(0.1)

stream.stop_stream()
stream.close()

#file.close()
p.terminate()
