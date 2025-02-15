import librosa
import numpy as np
import argparse
import sys

dtmf_freqs = {
    (697, 1209): '1', (697, 1336): '2', (697, 1477): '3',
    (770, 1209): '4', (770, 1336): '5', (770, 1477): '6',
    (852, 1209): '7', (852, 1336): '8', (852, 1477): '9',
    (941, 1209): '*', (941, 1336): '0', (941, 1477): '#'
}

low_freqs = [697, 770, 852, 941]
high_freqs = [1209, 1336, 1477]

def get_closest_frequency(freq, freq_list):
    return min(freq_list, key=lambda x: abs(x - freq))

def detect_key(low_freq, high_freq):

    low = get_closest_frequency(low_freq, low_freqs)
    high = get_closest_frequency(high_freq, high_freqs)
    return dtmf_freqs.get((low, high), -1)

def key_tone_recognition(audio_array):
    # Unpack audio and sample rate
    signal, sr = audio_array
    frame_size = int(sr / 64)  # 750 samples per frame
    num_frames = len(signal) // frame_size

    # RMS threshold for silence
    rms_threshold = 0.1

    output = []

    for i in range(num_frames):
        # Extract current frame
        frame = signal[i * frame_size:(i + 1) * frame_size]
        # Calculate RMS energy
        rms = np.sqrt(np.mean(frame**2))
        if rms < rms_threshold:
            # Silence detected
            output.append('-1')
            continue

        # Perform FFT
        fft_result = np.fft.rfft(frame)
        freqs = np.fft.rfftfreq(len(frame), 1 / sr)
        magnitudes = np.abs(fft_result)

        # get the highest peak in the low frequency band
        # convert freqs and magnitudes to map
        freqs_map = dict(zip(freqs, magnitudes))
        # get the key of the max value in the freqs_map where the key is between 600 and 1000
        low_peak_key = max({k: v for k, v in freqs_map.items() if 600 <= k <= 1000}.items(), key=lambda x: x[1])[0]
        high_peak_key = max({k: v for k, v in freqs_map.items() if 1100 <= k <= 1600}.items(), key=lambda x: x[1])[0]
        # Detect key based on frequency peaks
        detected_key = detect_key(low_peak_key, high_peak_key)
        output.append(str(detected_key))

    # Combine the results into the expected format
    return ' '.join(output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--audio_file', type = str, help = 'test file name', required = True)
    args = parser.parse_args()
    input_audio_array = librosa.load(args.audio_file, sr = 48000, dtype = np.float32) # audio file is numpy float array
    res = key_tone_recognition(input_audio_array)
    print(res,end=" ")
    