#!/bin/bash
# Moved from project root to scripts/
# Example script to demonstrate the use of the ATIS Whisper Synthetic Data Generator
# WITHOUT requiring a Gemini API key or SRT correction.
# This script will:
#   1. Run setup.sh (installs dependencies, builds DECtalk if needed)
#   2. Run the main pipeline to generate 2 ATIS samples with noise and SRTs (no SRT correction)

set -e

cd "$(dirname "$0")/.."

echo "[1/2] Running setup script (installs dependencies, builds DECtalk if needed)..."
bash scripts/setup.sh --no-gemini

echo "[2/2] Running the ATIS data pipeline (no Gemini API key required, no SRT correction)..."
python -m atiswhisper.main --output_dir ./data_no_gemini --samples 2 --generate_srt --add_noise

echo "Example run complete! Check the ./data_no_gemini directory for results."
