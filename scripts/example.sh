#!/bin/bash
# Moved from project root to scripts/
# Example script to demonstrate the use of the ATIS Whisper Synthetic Data Generator
# This script will:
#   1. Run setup.sh (installs dependencies, sets up API key, builds DECtalk if needed)
#   2. Run the main pipeline to generate 2 ATIS samples with noise and SRTs

set -e

cd "$(dirname "$0")/.."

echo "[1/2] Running setup script (installs dependencies, sets up API key, builds DECtalk if needed)..."
bash scripts/setup.sh

echo "[2/2] Running the ATIS data pipeline..."
python -m atiswhisper.main --output_dir ./data --generate_srt --add_noise --samples 3 --gemini_correction

echo "Example run complete! Check the ./data directory for results."
