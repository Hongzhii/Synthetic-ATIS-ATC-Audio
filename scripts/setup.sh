#!/bin/bash
# setup.sh
# This script sets up the environment for ATIS Whisper Synthetic Data Generator
# 1. Prompts for Google API key if not set
# 2. Exports the key to the user's shell profile
# 3. Installs Python dependencies
# 4. Builds DECtalk if not present

set -e


# Parse arguments
IGNORE_GEMINI_KEY=0
for arg in "$@"; do
  if [ "$arg" = "--no-gemini" ] || [ "$arg" = "--ignore-gemini-key" ]; then
    IGNORE_GEMINI_KEY=1
  fi
done

# 1. Prompt user to export GOOGLE_API_KEY manually, unless --no-gemini is set
if [ $IGNORE_GEMINI_KEY -eq 0 ]; then
  if [ -z "$GOOGLE_API_KEY" ]; then
    echo "\n[!] GOOGLE_API_KEY is not set."
    echo "Please export your Google Gemini API key before running the pipeline."
    echo "Example:"
    echo "  export GOOGLE_API_KEY=your_actual_api_key"
    echo "(You can add this line to your ~/.zshrc or ~/.bash_profile for persistence.)"
    exit 1
  else
    echo "GOOGLE_API_KEY is set."
  fi
else
  echo "[!] Skipping GOOGLE_API_KEY check due to --no-gemini flag."
fi

# 2. Install Python dependencies
if [ -f requirements.txt ]; then
  echo "Installing Python dependencies..."
  pip install uv
  uv pip install -r requirements.txt
else
  echo "requirements.txt not found!"
fi

# 3. Build DECtalk if not present
if [ ! -d "dectalk" ]; then
  echo "DECtalk not found. Running dec_talk_install.sh..."
  bash scripts/dec_talk_install.sh
else
  echo "DECtalk directory already exists. Skipping build."
fi

echo "Setup complete! You may need to restart your terminal for the API key to take effect."
