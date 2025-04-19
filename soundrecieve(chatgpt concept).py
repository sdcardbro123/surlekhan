import numpy as np
import librosa
import os
def detect_notes_by_chunk(filename, dur=0.5, sr=44100):
    y, sr = librosa.load(filename, sr=sr)
    samples_per_chunk = int(dur * sr)
    total_chunks = len(y) // samples_per_chunk
    notes = []

    for i in range(total_chunks):
        chunk = y[i * samples_per_chunk:(i + 1) * samples_per_chunk]
        if len(chunk) < samples_per_chunk:
            continue  # Skip last short chunk

        # Apply FFT
        fft = np.fft.fft(chunk)
        freqs = np.fft.fftfreq(len(chunk), 1/sr)
        magnitudes = np.abs(fft)

        # Use only the positive frequencies
        half = len(freqs) // 2
        freqs = freqs[:half]
        magnitudes = magnitudes[:half]

        # Find peak frequency
        peak_idx = np.argmax(magnitudes)
        peak_freq = freqs[peak_idx]

        # Convert to note name
        if peak_freq > 0:
            note = librosa.hz_to_note(peak_freq)
            notes.append(note)
        else:
            notes.append(None)

    return notes
notes = detect_notes_by_chunk("binoutput.wav", dur=0.5)
file = ''
for note in notes:
    if note == "C4":
        file += '0'
    elif note == "C5":
        file += '1'

def binary(filepath):
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"No such file: {filepath}")
    with open(filepath, 'rb') as f:
        byte_data = f.read()
    return ''.join(format(byte, '08b') for byte in byte_data)
x = r"C:\Users\s dhar\Desktop\sad.txt"
bin_data = binary(x)
if file == bin_data:
    print("yeeeeeeeeeeeeeeeeeehaw")
