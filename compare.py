import os
import re
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft
from scipy.signal import find_peaks, butter, sosfilt, windows
import soundfile as sf


# Function to list FLAC files in the current directory
def list_flac_files(directory):
    return [f for f in os.listdir(directory) if f.endswith('.flac')]


# Function to extract frequency range and spacing from file name
def extract_frequencies_from_name(file_name):
    pattern = r"(\d+\.\d+)kHz_to_(\d+\.\d+)kHz(?:_spacing_(\d+\.\d+)kHz)?(?:_regular|_max)?"
    match = re.search(pattern, file_name)
    if match:
        start_freq = float(match.group(1)) * 1000  # Convert to Hz
        end_freq = float(match.group(2)) * 1000  # Convert to Hz
        spacing = float(match.group(3)) * 1000 if match.group(3) else None  # Convert to Hz
        return start_freq, end_freq, spacing
    else:
        return None, None, None


# Function to apply a bandpass filter
def bandpass_filter(data, lowcut, highcut, fs, order=5):
    sos = butter(order, [lowcut, highcut], btype='band', fs=fs, output='sos')
    return sosfilt(sos, data)


# Function to calculate RMS amplitude
def calculate_rms(data):
    return np.sqrt(np.mean(data**2))


# Function to calculate spectral flatness
def calculate_spectral_flatness(data):
    fft_data = np.abs(fft(data))
    geometric_mean = np.exp(np.mean(np.log(fft_data + 1e-10)))
    arithmetic_mean = np.mean(fft_data)
    return geometric_mean / arithmetic_mean


# Function to calculate total power
def calculate_total_power(data):
    return np.sum(data**2)


# Function to apply a Hanning window
def apply_window(data):
    window = windows.hann(len(data))
    return data * window


# Function to plot the frequency spectrum with peaks
def plot_frequency_spectrum_with_peaks(audio_data, samplerate, title, lowcut=None, highcut=None, color='blue', alpha=1.0, offset=0):
    # Optionally filter the data
    if lowcut and highcut:
        audio_data = bandpass_filter(audio_data, lowcut, highcut, samplerate)

    # Apply windowing
    audio_data = apply_window(audio_data)

    # Perform FFT
    n = len(audio_data)
    yf = np.abs(fft(audio_data))[:n // 2] / n  # Normalize FFT
    xf = np.linspace(0, samplerate / 2, n // 2)  # Frequency axis in Hz

    # Restrict data to the specified frequency range
    if lowcut and highcut:
        mask = (xf >= lowcut) & (xf <= highcut)
        xf = xf[mask]
        yf = yf[mask]

    # Find peaks within the restricted range
    peaks, _ = find_peaks(20 * np.log10(yf + 1e-10), height=-80, distance=100)

    # Plot spectrum
    plt.plot(xf / 1000 + offset, 20 * np.log10(yf + 1e-10), label=title, color=color, alpha=alpha)
    plt.scatter(xf[peaks] / 1000 + offset, 20 * np.log10(yf[peaks] + 1e-10), color=color, s=10, label=f"Peaks ({title})", alpha=alpha)
    for peak in peaks:
        plt.annotate(f"{xf[peak] / 1000 + offset:.2f} kHz", (xf[peak] / 1000 + offset, 20 * np.log10(yf[peak]) + 2), fontsize=8, alpha=alpha)

    plt.xlabel("Frequency (kHz)")
    plt.ylabel("Magnitude (dB)")
    plt.title("Frequency Spectrum Comparison")
    plt.grid()
    plt.legend(loc="upper right")  # Explicit location for legend
    plt.xlim([lowcut / 1000, highcut / 1000])  # Restrict x-axis to the file's frequency range


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
        mode = input("Do you want to analyze a single FLAC file or compare two? (Enter 's' for single, 'c' for compare): ").strip().lower()
        if mode in ['s', 'c']:
            break
        print("Invalid input. Please enter 's' for single or 'c' for compare.")

    if mode == 's':
        # Single file mode
        print("\nSelect the FLAC file to analyze:")
        file = select_file(flac_files)
        if file:
            start_freq, end_freq, _ = extract_frequencies_from_name(file)
            print(f"\nAnalyzing frequency spectrum for: {file}")
            data, samplerate = sf.read(file)

            plt.figure(figsize=(12, 6))
            plot_frequency_spectrum_with_peaks(data, samplerate, file, lowcut=start_freq, highcut=end_freq, color='blue', alpha=0.8)
            plt.show()

            rms = calculate_rms(data)
            flatness = calculate_spectral_flatness(data)
            power = calculate_total_power(data)

            print(f"\nMetrics for {file}:")
            print(f"RMS Amplitude: {rms:.4f}")
            print(f"Spectral Flatness: {flatness:.4f}")
            print(f"Total Power: {power:.4f}")

    elif mode == 'c':
        # Comparison mode
        print("\nSelect the first file for comparison:")
        file1 = select_file(flac_files)
        print("\nSelect the second file for comparison:")
        file2 = select_file(flac_files)

        if file1 and file2:
            start_freq1, end_freq1, _ = extract_frequencies_from_name(file1)
            start_freq2, end_freq2, _ = extract_frequencies_from_name(file2)

            # Restrict to the overlapping frequency range
            lowcut = max(start_freq1, start_freq2)
            highcut = min(end_freq1, end_freq2)

            print(f"\nComparing {file1} and {file2}")
            data1, samplerate1 = sf.read(file1)
            data2, samplerate2 = sf.read(file2)

            plt.figure(figsize=(12, 6))
            plot_frequency_spectrum_with_peaks(data1, samplerate1, file1, lowcut=lowcut, highcut=highcut, color='blue', alpha=0.8, offset=0)
            plot_frequency_spectrum_with_peaks(data2, samplerate2, file2, lowcut=lowcut, highcut=highcut, color='red', alpha=0.8, offset=0.01)
            plt.show()

            rms1 = calculate_rms(data1)
            rms2 = calculate_rms(data2)
            flatness1 = calculate_spectral_flatness(data1)
            flatness2 = calculate_spectral_flatness(data2)
            power1 = calculate_total_power(data1)
            power2 = calculate_total_power(data2)

            print("\nComparison Metrics:")
            print(f"{file1}: RMS={rms1:.4f}, Flatness={flatness1:.4f}, Power={power1:.4f}")
            print(f"{file2}: RMS={rms2:.4f}, Flatness={flatness2:.4f}, Power={power2:.4f}")


if __name__ == "__main__":
    main()
