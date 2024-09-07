import wave
import numpy as np

# harmonics added on top of base frequency in touple [relative frequency, relative amplitude]
harms = [
    [1, 1],
    [2, 0.017783],
    [2.6, 0.00631],
    [3, 0.056234],
    [4, 0.01],
    [5, 0.022387],
    [5.3, 0.019953],
    [6, 0.005012],
    [7, 0.002818],
    [7.4, 0.004467],
    [9.5, 0.002239],
    [11.67, 0.001585],
    [14, 0.001259]
]

# base frequencies of each chord
chords = [
    [174.6141], # Dm chord: (F3, G#3, C4, F4)
    [174.6141, 207.6523], # Dm chord: (F3, G#3, C4, F4)
    [174.6141, 207.6523, 261.6256], # Dm chord: (F3, G#3, C4, F4)
    [174.6141, 207.6523, 261.6256, 349.2282], # Dm chord: (F3, G#3, C4, F4)
    [174.6141, 207.6523, 261.6256, 349.2282], # Dm chord: (F3, G#3, C4, F4)
    [195.9977, 233.0819, 293.6648, 391.9954], # Em chord: (G3, A#3, D4, G4)
    [207.6523, 261.6256, 311.127, 415.3047], # F chord: (G#3, C4, D#4, G#4)
    [233.0819, 293.6648, 349.2282, 466.1638], # G chord: (A#3, D4, F4, A#4)
    [261.6256, 329.6276, 391.9954, 523.2511], # A chord: (C4, E4, G4, C5)
    [261.6256, 329.6276, 391.9954, 523.2511] # A chord: (C4, E4, G4, C5)
]


# The callback function for continuous playback
def amp_function(time, chord_index):
    global chords, harms
    # ampl = np.sum([[(hrm[1] * np.sin(2 * np.pi * hrm[0] * freq * time)) for hrm in harms] for freq in chords])
    ampl = 0
    for freq in chords[chord_index]:
        for hrm in harms:
            ampl += (hrm[1] * np.sin(2 * np.pi * hrm[0] * freq * time))
    if chord_index < 4:
        volume = 0.02
    elif chord_index == 4:
        volume = min(1, 0.2 + (time / 4))
    elif chord_index < 9:
        volume = 1
    else:
        volume = max(1 - time / 4, 0)
    ampl *= (volume / len(chords[chord_index])  # Normalize amplitude
    return ampl

def generate_wav(filename, duration, chord_index, sample_rate=44100):
    # Total number of samples
    num_samples = int(sample_rate * duration)

    # Time points
    t_values = np.linspace(0, duration, num_samples, endpoint=False)

    # Generate samples using your function
    samples = np.array([amp_function(t, chord_index) for t in t_values], dtype=np.float32)

    # Normalize to the range of 16-bit integers (-32768 to 32767)
    samples = np.int16(samples / np.max(np.abs(samples)) * 32767)

    # Write to WAV file
    with wave.open(filename, 'w') as wav_file:
        # Set parameters: 1 channel, 2 bytes per sample, sample rate, num samples, no compression
        wav_file.setparams((1, 2, sample_rate, num_samples, 'NONE', 'not compressed'))

        # Write frames as byte string
        wav_file.writeframes(samples.tobytes())


# Example of a simple sine wave as the amplitude function
import math


# Generate a 5 second sine wave at 440Hz
for i in range(len(chords)):
    generate_wav("C:\\Users\\Andrew\\Downloads\\sine_wave_" + str(i) + ".wav", 4, i)
