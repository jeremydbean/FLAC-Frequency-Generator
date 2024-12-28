
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
