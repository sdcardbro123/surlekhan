import numpy as np
import librosa
import os

def detectnotesbychunk(filename, dur=0.5, sr=44100):
    audio, sr = librosa.load(filename, sr=sr)
    samples = int(dur * sr)
    chunks = len(audio) // samples
    notes = []

    for i in range(chunks):
        chunk = audio[i * samples:(i + 1) * samples]
        if len(chunk) < samples:
            continue

        fft = np.fft.fft(chunk)
        freqs = np.fft.fftfreq(len(chunk), 1 / sr)
        mags = np.abs(fft)

        half = len(freqs) // 2
        freqs = freqs[:half]
        mags = mags[:half]

        peak = freqs[np.argmax(mags)]

        if peak > 0:
            notes.append(librosa.hz_to_note(peak))
        else:
            notes.append(None)

    return notes

audiopath = input("Enter wav file path: ")
notes = detectnotesbychunk(audiopath, dur=0.5)

filedata = ""
for note in notes:
    if note == "C4":
        filedata += "0"
    elif note == "C5":
        filedata += "1"

def binarytotext(binstring, outpath):
    bytesdata = []
    for i in range(0, len(binstring), 8):
        byte = binstring[i:i + 8]
        if len(byte) == 8:
            bytesdata.append(int(byte, 2))
    with open(outpath, "wb") as f:
        f.write(bytes(bytesdata))

outputpath = "recovered.txt"
binarytotext(filedata, outputpath)
