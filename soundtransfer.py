import sounddevice as sd
import numpy as np
import os
import random
from scipy.io.wavfile import write

notes = [
    261.63,
    293.66,
    329.63,
    349.23,
    392.00,
    440.00,
    493.88,
    523.25
]

dur = 0.5
sample_rate = 44100
volume = 0.5

def play_note(freq, duration=dur, volume=volume, sample_rate=sample_rate):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = volume * np.sin(2 * np.pi * freq * t)
    sd.play(wave, sample_rate)
    sd.wait()

def binary(path):
    if not os.path.isfile(path):
        raise FileNotFoundError(path)
    with open(path, 'rb') as f:
        data = f.read()
    return ''.join(format(b, '08b') for b in data)

def chunk(bits):
    out = []
    for i in range(0, len(bits), 3):
        out.append(bits[i:i+3].ljust(3, '0'))
    return out

def triplet_to_note(seed):
    shift = (seed - 1) % 8
    base = notes[shift:] + notes[:shift]
    table = {
        format(i, '03b'): base[i]
        for i in range(8)
    }
    return table

def encode(bits, seed):
    pieces = chunk(bits)
    table = triplet_to_note(seed)
    audio = np.array([], dtype=np.float32)
    for triplet in pieces:
        freq = table[triplet]
        t = np.linspace(0, dur, int(sample_rate * dur), endpoint=False)
        wave = volume * np.sin(2 * np.pi * freq * t)
        audio = np.concatenate((audio, wave))
    return audio

def save(audio, filename):
    out = np.int16(audio * 32767)
    write(filename, sample_rate, out)

file_path = r"C:\Users\s dhar\Desktop\sad.txt"
seed = random.randint(1, 10)

bits = binary(file_path)
waveform = encode(bits, seed)
save(waveform, "encoded_output.wav")
