import os
import numpy as np
import soundfile as sf


# Function to generate a sine wave
def generate_sine_wave(frequency, duration, sample_rate=48000):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    sine_wave = 0.9 * np.sin(2 * np.pi * frequency * t)  # Amplitude set to 0.9 for headroom
    return sine_wave


# Function to save FLAC incrementally
def save_flac_incrementally(filename, frequencies, duration, sample_rate, bit_depth):
    with sf.SoundFile(filename, mode='w', samplerate=sample_rate, channels=1, subtype=bit_depth, format='FLAC') as f:
        for freq in frequencies:
            print(f"Generating frequency: {freq:.3f} kHz")
            sine_wave = generate_sine_wave(freq * 1000, duration, sample_rate)  # Convert kHz to Hz
            f.write(sine_wave)  # Write each segment directly to the file
    print(f"Generated FLAC file: {filename}")


# Function to generate an SRT subtitle file
def save_srt(filename, frequencies, duration):
    with open(filename, "w") as f:
        for i, freq in enumerate(frequencies):
            start_time = i * duration
            end_time = (i + 1) * duration
            spacing = frequencies[1] - frequencies[0] if len(frequencies) > 1 else 0
            f.write(f"{i + 1}\n")
            f.write(f"{format_time(start_time)} --> {format_time(end_time)}\n")
            f.write(f"Frequency: {freq:.3f} kHz, Spacing: {spacing:.3f} kHz\n\n")
    print(f"Generated subtitle file: {filename}")


# Helper function to format time for SRT
def format_time(seconds):
    ms = int((seconds % 1) * 1000)
    s = int(seconds) % 60
    m = (int(seconds) // 60) % 60
    h = int(seconds) // 3600
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


# Main logic
def main():
    print("Welcome to the FLAC generator.")
    
    # Ask for FLAC quality
    while True:
        quality = input("Would you like regular (48kHz, 16-bit) or max (192kHz, 24-bit) FLAC quality? (Enter 'r' for regular or 'm' for max): ").strip().lower()
        if quality in ['r', 'm']:
            break
        print("Invalid input. Please enter 'r' for regular or 'm' for max.")
    
    if quality == 'r':
        sample_rate = 48000
        bit_depth = 'PCM_16'
        quality_label = 'regular'
    elif quality == 'm':
        sample_rate = 192000
        bit_depth = 'PCM_24'
        quality_label = 'max'
    
    # Select mode
    while True:
        mode = input("Do you want to generate a single file, a range, or a changing frequency file? (Enter 's' for single, 'r' for range, or 'c' for changing): ").strip().lower()
        if mode in ['s', 'r', 'c']:
            break
        print("Invalid input. Please enter 's' for single, 'r' for range, or 'c' for changing.")
    
    if mode == 's':
        # Single frequency mode
        frequency = float(input("Enter the frequency in kHz (e.g., 17.4 for 17.4 kHz): "))
        duration = float(input("Enter the duration of the audio in seconds: "))
        flac_filename = f"{frequency:.3f}kHz_single_{quality_label}.flac"
        sine_wave = generate_sine_wave(frequency * 1000, duration, sample_rate)
        sf.write(flac_filename, sine_wave, sample_rate, subtype=bit_depth)
        print(f"Generated single frequency file: {flac_filename}")
    
    elif mode == 'r':
        # Range mode
        start_frequency_khz = float(input("Enter the starting frequency in kHz (e.g., 15 for 15 kHz): "))
        end_frequency_khz = float(input("Enter the ending frequency in kHz (e.g., 19 for 19 kHz): "))
        spacing_khz = float(input("Enter the spacing between frequencies in kHz (e.g., 0.5 for 0.5 kHz): "))
        duration = float(input("Enter the duration of each frequency in seconds: "))
        
        frequencies_khz = np.arange(start_frequency_khz, end_frequency_khz + spacing_khz, spacing_khz)
        flac_filename = f"{start_frequency_khz:.3f}kHz_to_{end_frequency_khz:.3f}kHz_spacing_{spacing_khz:.3f}kHz_{quality_label}.flac"
        srt_filename = flac_filename.replace(".flac", ".srt")
        
        save_flac_incrementally(flac_filename, frequencies_khz, duration, sample_rate, bit_depth)
        save_srt(srt_filename, frequencies_khz, duration)
    
    elif mode == 'c':
        # Changing frequency mode
        start_frequency_khz = float(input("Enter the starting frequency in kHz (e.g., 15 for 15 kHz): "))
        end_frequency_khz = float(input("Enter the ending frequency in kHz (e.g., 19 for 19 kHz): "))
        spacing_khz = float(input("Enter the spacing between frequencies in kHz (e.g., 0.5 for 0.5 kHz): "))
        freq_duration = float(input("Enter the duration to play each frequency in seconds: "))
        
        frequencies_khz = np.arange(start_frequency_khz, end_frequency_khz + spacing_khz, spacing_khz)
        audio_data = np.concatenate([generate_sine_wave(freq * 1000, freq_duration, sample_rate) for freq in frequencies_khz])
        
        flac_filename = f"{start_frequency_khz:.3f}kHz_to_{end_frequency_khz:.3f}kHz_changing_{quality_label}.flac"
        srt_filename = flac_filename.replace(".flac", ".srt")
        
        sf.write(flac_filename, audio_data, sample_rate, subtype=bit_depth)
        save_srt(srt_filename, frequencies_khz, freq_duration)
        print(f"Generated changing frequency file: {flac_filename}")


if __name__ == "__main__":
    main()

