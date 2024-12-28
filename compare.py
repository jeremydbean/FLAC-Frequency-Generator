import os
import re
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft
from scipy.signal import butter, sosfilt, windows
import soundfile as sf


# Function to list FLAC files in the current directory
def list_flac_files(directory):
    return [f for f in os.listdir(directory) if f.endswith('.flac')]


# Function to extract frequency range and spacing from file name
def extract_frequencies_from_name(file_name):
    pattern = r"(\d+\.\d+)kHz_to_(\d+\.\d+)kHz_spacing_(\d+\.\d+)kHz"
    match = re.search(pattern, file_name)
    if match:
        start_freq = float(match.group(1)) * 1000  # Convert to Hz
        end_freq = float(match.group(2)) * 1000  # Convert to Hz
        spacing = float(match.group(3)) * 1000  # Convert to Hz
        return start_freq, end_freq, spacing
    else:
        return None, None, None


# Function to apply a bandpass filter to isolate the target frequency range
def bandpass_filter(data, lowcut, highcut, fs, order=5):
    sos = butter(order, [lowcut, highcut], btype='band', fs=fs, output='sos')
    return sosfilt(sos, data)


# Function to apply a window to reduce spectral leakage
def apply_window(data):
    window = windows.hann(len(data))
    return data * window


# Function to plot the frequency spectrum
def plot_frequency_spectrum(audio_data, samplerate, title, lowcut=None, highcut=None, color='blue'):
    # Optionally filter the data
    if lowcut and highcut:
        audio_data = bandpass_filter(audio_data, lowcut, highcut, samplerate)

    # Apply windowing to reduce spectral leakage
    audio_data = apply_window(audio_data)

    # Perform FFT
    n = len(audio_data)
    yf = np.abs(fft(audio_data))[:n // 2] / n  # Normalize the FFT
    xf = np.linspace(0, samplerate / 2, n // 2) / 1000  # Convert to kHz

    # Plot the spectrum
    plt.plot(xf, 20 * np.log10(yf + 1e-10), label=title, color=color)
    plt.xlabel("Frequency (kHz)")
    plt.ylabel("Magnitude (dB)")
    plt.title(f"Frequency Spectrum: {title}")
    plt.xlim([lowcut / 1000 if lowcut else 0, highcut / 1000 if highcut else samplerate / 2000])  # Restrict x-axis
    plt.legend()
    plt.grid()


# Function to get user selection from a list of files
def select_file(file_list):
    if not file_list:
        print("No FLAC files found in the current directory.")
        return None
    print("\nFLAC files found:")
    for i, file in enumerate(file_list, start=1):
        print(f"{i}. {file}")
    while True:
        try:
            choice = int(input("Select a FLAC file by number: ")) - 1
            if 0 <= choice < len(file_list):
                return file_list[choice]
            else:
                print("Invalid choice. Please select a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")


# Main logic
def main():
    current_directory = os.getcwd()
    flac_files = list_flac_files(current_directory)

    if not flac_files:
        print("No FLAC files found. Please ensure there are FLAC files in the current directory.")
        return

    # Prompt user to view a single file or compare two
    while True:
        mode = input("Do you want to view a single FLAC file or compare two? (Enter 'single' or 'compare'): ").strip().lower()
        if mode in ['single', 'compare']:
            break
        print("Invalid input. Please enter 'single' or 'compare'.")

    if mode == 'single':
        # Single file mode
        file = select_file(flac_files)
        if file:
            # Automatically extract frequency range and spacing from the file name
            start_freq, end_freq, spacing = extract_frequencies_from_name(file)
            if start_freq and end_freq:
                print(f"Automatically detected frequency range: {start_freq / 1000:.3f} kHz to {end_freq / 1000:.3f} kHz")
                print(f"Spacing: {spacing / 1000:.3f} kHz")
            else:
                print("Could not detect frequency range from file name. Please enter manually.")
                start_freq = float(input("Enter the lower bound of the frequency range to analyze (in Hz): "))
                end_freq = float(input("Enter the upper bound of the frequency range to analyze (in Hz): "))

            print(f"\nViewing frequency spectrum for: {file}")
            data, samplerate = sf.read(file)

            plt.figure(figsize=(12, 6))
            plot_frequency_spectrum(data, samplerate, file, lowcut=start_freq, highcut=end_freq, color='blue')
            plt.show()
        else:
            print("No file selected. Exiting.")

    elif mode == 'compare':
        # Comparison mode
        print("\nSelect the first file for comparison:")
        file1 = select_file(flac_files)
        print("\nSelect the second file for comparison:")
        file2 = select_file(flac_files)

        if file1 and file2:
            # Automatically extract frequency ranges from file names
            start_freq1, end_freq1, spacing1 = extract_frequencies_from_name(file1)
            start_freq2, end_freq2, spacing2 = extract_frequencies_from_name(file2)

            print(f"\nComparing {file1} ({start_freq1 / 1000:.3f} kHz to {end_freq1 / 1000:.3f} kHz)")
            print(f"With {file2} ({start_freq2 / 1000:.3f} kHz to {end_freq2 / 1000:.3f} kHz)")

            plt.figure(figsize=(12, 6))
            data1, samplerate1 = sf.read(file1)
            plot_frequency_spectrum(data1, samplerate1, f"{file1}", lowcut=start_freq1, highcut=end_freq1, color='blue')

            data2, samplerate2 = sf.read(file2)
            plot_frequency_spectrum(data2, samplerate2, f"{file2}", lowcut=start_freq2, highcut=end_freq2, color='red')
            plt.show()
        else:
            print("Comparison could not be completed. Ensure two files are selected.")


if __name__ == "__main__":
    main()

