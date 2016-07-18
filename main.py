import pyaudio
import wave
import os
from output import Output
from settings import SAMPLE_RATE, SAMPLE_WIDTH, BUFFER_SIZE
from mixer import MonoMixer, PolyMixer
from tkinter import *
from keys import map_keys
from presets import *


os.system('xset r off')

p = pyaudio.PyAudio()
mixer = MonoMixer(SMOOTH)
mixer.controller.portamento.value = 100.0
out = Output(mixer)

tk_root = Tk()
map_keys(tk_root, mixer.controller)

save_wav = True

if save_wav:
    file = wave.open('output.wav', 'wb')
    file.setframerate(SAMPLE_RATE)
    file.setsampwidth(SAMPLE_WIDTH)
    file.setnchannels(1)


def callback(input_data, frame_count, time_info, status):
    data = out.get_chunk(frame_count)
    if save_wav:
        file.writeframes(data)
    return data, pyaudio.paContinue


stream = p.open(format=p.get_format_from_width(SAMPLE_WIDTH),
                channels=1,
                rate=SAMPLE_RATE,
                frames_per_buffer=BUFFER_SIZE,
                output=True,
                stream_callback=callback,
                )

stream.start_stream()
tk_root.mainloop()



#while stream.is_active():
#    pitch = float(input("..."))
#    mixer.note_on(100, pitch)
#    input("...")
#    mixer.note_off()


stream.stop_stream()
stream.close()
os.system('xset r on')

if save_wav:
    file.close()

p.terminate()
