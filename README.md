
# FLAC Frequency Generator

This Python script generates **FLAC audio files** containing sine waves at specific frequencies. You can create files in either **regular quality (48 kHz, 16-bit)** or **maximum quality (192 kHz, 24-bit)**. The script supports three modes: **Single Frequency**, **Range of Frequencies**, and **Changing Frequency**. It also generates accompanying subtitle files (`.srt`) for range and changing modes, displaying the frequency and duration at each step.

## Features

- **Choose Audio Quality**:
  - **Regular**: 48 kHz sample rate, 16-bit depth.
  - **Maximum**: 192 kHz sample rate, 24-bit depth.

- **Modes**:
  1. **Single Frequency**: Generate a FLAC file containing one sine wave at a fixed frequency.
  2. **Range of Frequencies**: Create a FLAC file with multiple frequencies, each lasting a specified duration, along with a matching subtitle file.
  3. **Changing Frequency**: Generate a FLAC file where the frequency changes continuously over a specified range, with optional spacing between steps, and include a matching subtitle file.

- **Dynamic File Naming**:
  - File names include the selected quality (`regular` or `max`), mode, and frequency range.

## Requirements

- Python 3.6 or later
- Required Python libraries:
  - `numpy`
  - `soundfile`

Install the dependencies using pip:
```bash
pip install numpy soundfile
```

## How to Use

### 1. Run the Script
Run the script from your terminal:
```bash
python3 flac_frequency_generator.py
```

### 2. Select FLAC Quality
You’ll be prompted to choose the audio quality:
- Enter `r` for **regular quality** (48 kHz, 16-bit).
- Enter `m` for **maximum quality** (192 kHz, 24-bit).

### 3. Select Mode
Choose the type of file you want to generate:
- Enter `s` for **Single Frequency**.
- Enter `r` for **Range of Frequencies**.
- Enter `c` for **Changing Frequency**.

### Modes Explained

#### Single Frequency
- Generates a single sine wave at a fixed frequency for a specified duration.
- **Prompted Inputs**:
  - Frequency in kHz (e.g., `17.4` for 17.4 kHz).
  - Duration in seconds (e.g., `10`).
- **Example Output**:
  - `17.400kHz_single_regular.flac` (for regular quality).

#### Range of Frequencies
- Creates a FLAC file with sine waves at multiple frequencies, spaced evenly, each lasting a specified duration.
- Generates an accompanying `.srt` subtitle file to display the frequency and duration at each step.
- **Prompted Inputs**:
  - Start and end frequencies in kHz (e.g., `15` to `19` for 15 kHz to 19 kHz).
  - Spacing between frequencies in kHz (e.g., `0.5` for 0.5 kHz).
  - Duration for each frequency in seconds (e.g., `2`).
- **Example Output**:
  - `15.000kHz_to_19.000kHz_spacing_0.500kHz_max.flac`
  - `15.000kHz_to_19.000kHz_spacing_0.500kHz_max.srt`

#### Changing Frequency
- Creates a FLAC file where the frequency changes step-by-step over a range, with each step lasting a specified duration.
- Generates an accompanying `.srt` subtitle file to display the frequency and duration at each step.
- **Prompted Inputs**:
  - Start and end frequencies in kHz (e.g., `15` to `19` for 15 kHz to 19 kHz).
  - Spacing between frequencies in kHz (e.g., `0.5` for 0.5 kHz).
  - Duration for each step in seconds (e.g., `2`).
- **Example Output**:
  - `15.000kHz_to_19.000kHz_changing_regular.flac`
  - `15.000kHz_to_19.000kHz_changing_regular.srt`

### 4. View Output
The generated FLAC and subtitle files are saved in the current working directory. File names include details such as frequency, range, spacing, and quality.

## Example Workflow

1. Run the script:
   ```bash
   python3 flac_frequency_generator.py
   ```
2. Select audio quality:
   - Enter `r` for regular or `m` for max.
3. Choose a mode:
   - Enter `s` for Single Frequency.
   - Enter `r` for Range of Frequencies.
   - Enter `c` for Changing Frequency.
4. Follow the prompts to input parameters (frequency, range, duration, etc.).
5. View the generated files in the current directory.

## License

This script is provided under the MIT License. You are free to use, modify, and distribute it.



-----------------------



# FLAC File Analyzer and Comparator (compare.py)

This script analyzes and compares FLAC files by visualizing their frequency
spectrum, peaks, and calculating metrics such as RMS amplitude, spectral
flatness, and total power.

## Features

  1. **Analyze a Single FLAC File** : 
     * Visualize the frequency spectrum of a single FLAC file.
     * Identify and annotate prominent frequency peaks.
     * Calculate and display metrics: 
       * **RMS Amplitude** : Measures the signal's power.
       * **Spectral Flatness** : Indicates how noise-like or tonal the spectrum is.
       * **Total Power** : Sum of the squared amplitudes of the signal.
  2. **Compare Two FLAC Files** : 
     * Overlay frequency spectra of two FLAC files for comparison.
     * Annotate peaks for both files.
     * Restrict the comparison to the overlapping frequency range specified in the file names.
     * Display metrics for both files: 
       * RMS Amplitude
       * Spectral Flatness
       * Total Power
  3. **Automatic Frequency Range Detection** : 
     * Extract frequency range and spacing from file names (e.g., `15.000kHz_to_19.000kHz_spacing_0.125kHz.flac`).

## Prerequisites

  * **Python 3.7 or later**
  * Required Python Libraries: 
    * `numpy`
    * `matplotlib`
    * `scipy`
    * `soundfile`

Install the required libraries with:

    
    
    pip install numpy matplotlib scipy soundfile

## Usage Instructions

  1. **Ensure your FLAC files are in the same directory as the script**.
  2. Run the script: 
    
        python3 compare.py

  3. Choose whether to analyze a single file or compare two: 
     * Enter `s` to analyze a single file.
     * Enter `c` to compare two files.

### Single File Analysis

  * Select a file by entering the number corresponding to the file in the list.
  * The script will: 
    * Display the frequency spectrum with peaks annotated.
    * Calculate and display RMS amplitude, spectral flatness, and total power.

### Comparing Two Files

  * Select two files by entering their numbers from the list.
  * The script will: 
    * Overlay the frequency spectra of both files.
    * Annotate peaks for both files with a slight offset to avoid overlap.
    * Calculate and display metrics for both files.

## Output

  * **Plots** : 
    * Frequency spectrum with peaks annotated.
    * Overlay of two spectra for comparison (in comparison mode).
  * **Metrics** : 
    * RMS Amplitude
    * Spectral Flatness
    * Total Power

## File Name Format

The script extracts frequency range and spacing information from the file
name. Ensure your files follow this format:

    
    
    <start_frequency>kHz_to_<end_frequency>kHz_spacing_<spacing>kHz_<type>.flac

For example:

    
    
    15.000kHz_to_19.000kHz_spacing_0.125kHz_max.flac

## Example Outputs

### Single File

  * Frequency spectrum with annotated peaks.
  * RMS amplitude, spectral flatness, and total power.

### Comparison

  * Overlayed frequency spectra with annotated peaks.
  * Metrics for both files, displayed side by side.

* * *

For any issues or suggestions, feel free to reach out!
