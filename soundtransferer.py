import sounddevice as sd
import numpy as np
import os
from scipy.io.wavfile import write

def play_note(frequency, duration=0.5, volume=0.5, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    waveform = volume * np.sin(2 * np.pi * frequency * t)
    sd.play(waveform, sample_rate)
    sd.wait()

def c(duration=0.5): play_note(261.63, duration)
def d(duration=0.5): play_note(293.66, duration)
def e(duration=0.5): play_note(329.63, duration)
def f(duration=0.5): play_note(349.23, duration)
def g(duration=0.5): play_note(392.00, duration)
def a(duration=0.5): play_note(440.00, duration)
def b(duration=0.5): play_note(493.88, duration)
def chigh(duration=0.5): play_note(523.25, duration)

dur = 0.5
sample_rate = 44100
volume = 0.5

def binary(filepath):
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"No such file: {filepath}")
    with open(filepath, 'rb') as f:
        byte_data = f.read()
    return ''.join(format(byte, '08b') for byte in byte_data)

def genaudio(binstring, dur, sample_rate, volume):
    totalwave = np.array([], dtype=np.float32)
    for bit in binstring:
        freq = 261.63 if bit == '0' else 523.25
        t = np.linspace(0, dur, int(sample_rate * dur), endpoint=False)
        wave = volume * np.sin(2 * np.pi * freq * t)
        totalwave = np.concatenate((totalwave, wave))
    return totalwave


def save(binstring, filename='out.wav'):
    waveform = genaudio(binstring, dur, sample_rate, volume)
    waveform_int16 = np.int16(waveform * 32767)
    write(filename, sample_rate, waveform_int16)
    print(f"Saved: {filename}")


x = r"C:\Users\s dhar\Desktop\sad.txt"
bin_data = binary(x)
save(bin_data, "binoutput.wav")
