# ATIS Whisper Synthetic Data Generator

> **Python Version Requirement:** This project supports only Python versions >=3.6 and <3.10. Please ensure your Python environment meets this requirement.

> **Note:** This repository has only been tested in Linux and macOS environments. Windows support has not been tested yet.

## Motivation
There is a significant shortage of publicly available ATIS (Automatic Terminal Information Service) audio data for training speech-to-text models like OpenAI Whisper. ATIS broadcasts are crucial for pilots, and the "Huge Harry" voice (from the DECtalk TTS system) is commonly used in the US for these transmissions. This project generates synthetic ATIS audio and transcript pairs using the Huge Harry voice, enabling:

- Training and evaluation of ASR (Automatic Speech Recognition) models, especially Whisper, for ATIS transcription.
- Use in flight simulators, aircraft games, or any application requiring realistic ATIS audio.

## Features
- **Synthetic ATIS Transcript Generation:** Randomized, realistic ATIS messages.
- **TTS Audio Synthesis:** Uses DECtalk's Huge Harry voice (via the `dist/` folder, see credits below).
- **Noise Augmentation:** Add Gaussian noise to audio for robust model training.
- **SRT Generation:** Generate SRT subtitles using OpenAI Whisper CLI.
- **SRT Correction (Optional, Gemini API key required):** Optionally correct SRTs using Gemini API and ground-truth transcripts. This is highly recommended if you plan to use the audio SRT pairs for fine-tuning a transcription model.

## Usage

You can run the pipeline with or without SRT correction (Gemini API key required only for SRT correction).

### Example 1: With SRT Correction (requires Gemini API key)

Before running the pipeline, you must manually export your Google Gemini API key as an environment variable. Copy and paste the following command into your terminal, replacing `your_actual_api_key` with your key:

```bash
export GOOGLE_API_KEY=your_actual_api_key
```

You can add this line to your `~/.zshrc` or `~/.bash_profile` to make it persistent across terminal sessions.

You can see a quick example by running:
```bash
bash scripts/example.sh
```
This will run the setup script, install dependencies, check for your Google API key, build DECtalk, and generate a small dataset in the `./data` directory.

**Manual setup:**
1. **Run the setup script:**
    ```bash
    bash setup.sh
    ```
    - This will check for your Google API key (for Gemini) in your environment, install Python dependencies, and build DECtalk if needed. If the key is not set, you will be prompted to export it manually.
2. **Run the pipeline:**
    ```bash
    python main.py --output_dir ./data --samples 100 --generate_srt --add_noise
    ```
    - `--output_dir`: Where to store generated data
    - `--samples`: Number of ATIS samples to generate
    - `--generate_srt`: Generate SRTs and correct them with Gemini API
    - `--add_noise`: Add noise to synthesized audio

### Example 2: Without SRT Correction (no Gemini API key required)

You can generate synthetic ATIS data, audio, and SRTs without using the Gemini API by running:
```bash
bash scripts/example_no_gemini.sh
```
This will run the setup script, install dependencies, build DECtalk, and generate a small dataset (including SRTs, but without SRT correction) in the `./data_no_gemini` directory.

**Manual setup:**
1. **Run the setup script:**
    ```bash
    bash scripts/setup.sh
    ```
    - This will install Python dependencies and build DECtalk if needed. If you want SRT correction, ensure your Google API key is exported as described below.
2. **Run the pipeline:**
    ```bash
    python -m atiswhisper.main --output_dir ./data --samples 100 --generate_srt --add_noise
    ```
    - `--output_dir`: Where to store generated data
    - `--samples`: Number of ATIS samples to generate
    - `--generate_srt`: Generate SRTs (correction only if API key is set)
    - `--add_noise`: Add noise to synthesized audio

## Google Gemini API Key Required (Only for SRT Correction)

If you want to use SRT correction, you must manually export your Google Gemini API key as an environment variable. Copy and paste the following command into your terminal, replacing `your_actual_api_key` with your key:

```bash
export GOOGLE_API_KEY=your_actual_api_key
```

You can add this line to your `~/.zshrc` or `~/.bash_profile` to make it persistent across terminal sessions.

You can see a quick example by running:
```bash
bash example.sh
```
This will run the setup script, install dependencies, check for your Google API key, build DECtalk, and generate a small dataset in the `./data` directory.

**Manual setup:**
1. **Run the setup script:**
    ```bash
    bash scripts/setup.sh
    ```
    - This will check for your Google API key (for Gemini) in your environment, install Python dependencies, and build DECtalk if needed. If the key is not set, you will be prompted to export it manually.
2. **Run the pipeline:**
    ```bash
    python -m atiswhisper.main --output_dir ./data --samples 100 --generate_srt --add_noise
    ```
    - `--output_dir`: Where to store generated data
    - `--samples`: Number of ATIS samples to generate
    - `--generate_srt`: Generate SRTs and correct them with Gemini API
    - `--add_noise`: Add noise to synthesized audio

## Folder Structure
- `atiswhisper/`: Main Python package
  - `main.py`: Main pipeline script (use `python -m atiswhisper.main`)
  - `synthesize_data.py`: Synthetic ATIS transcript and audio generation
  - `noise.py`: Audio noise augmentation
  - `gemini_api.py`: SRT correction using Gemini API
- `scripts/`: Shell scripts and utilities
  - `setup.sh`: Unified setup script (API key, dependencies, DECtalk build)
  - `dec_talk_install.sh`: (Called by setup.sh) Script to build and install DECtalk locally
  - `example.sh`, `example_no_gemini.sh`: Example usage scripts
- `dectalk/dist/`: (Generated) Contains DECtalk binaries
- `data/`, `data_no_gemini/`: Output data (audio, transcripts, SRTs, etc.)

## Credits
- **DECtalk TTS (Huge Harry voice):** The `dist/` folder is generated by building from the [dectalk/dectalk](https://github.com/dectalk/dectalk) repository. All rights and credits belong to the original authors.

## License
All code in this repository (except DECtalk binaries and code) is licensed under the MIT License. See the LICENSE file for details.

**Important:**
- The DECtalk binaries and code in the `dist/` folder are proprietary and are **not** covered by the MIT License. They are subject to the following license terms:
  - Copyright (C) 2002-2003 FONIX Corporation,   All rights reserved.
  - Copyright (C) 2000-2001 FORCE Computers Inc,   All rights reserved.
  - Copyright (C) 1999 SMART Modular Technologies,  All rights reserved.
  - Use, copying, or distribution is only allowed with a valid written license from FONIX or an authorized sublicensor.
  - This software is provided "as is" and without any express or implied warranties.

You must obtain DECtalk binaries and comply with their license separately. They are not distributed under the MIT License.
