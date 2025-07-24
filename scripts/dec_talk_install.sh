#!/bin/bash
# Moved from project root to scripts/

REPO_URL="https://github.com/dectalk/dectalk.git"
REPO_DIR="dectalk"
DIST_DIR="dist"

# Detect OS
OS="$(uname -s)"

if [[ "$OS" == "Darwin" ]]; then
    echo "Detected macOS"
    xcode-select -p &>/dev/null || xcode-select --install
    git clone "$REPO_URL"
    cd "$REPO_DIR/src"
    autoreconf -si
    ./configure
    make -j
    cd ..
    echo "DECtalk built for macOS. Binaries are in dectalk/dist/"
elif [[ "$OS" == "Linux" ]]; then
    echo "Detected Linux"
    if command -v apt-get &>/dev/null; then
        sudo apt-get update
        sudo apt-get install -y build-essential libasound2-dev libpulse-dev libgtk2.0-dev unzip git autoconf automake libtool
    fi
    git clone "$REPO_URL"
    cd "$REPO_DIR/src"
    ./autogen.sh
    ./configure
    make -j
    cd ..
    echo "DECtalk built for Linux.  Binaries are in dectalk/dist/"
elif grep -qi microsoft /proc/version 2>/dev/null; then
    echo "Detected Windows Subsystem for Linux (WSL)"
    sudo apt-get update
    sudo apt-get install -y build-essential libasound2-dev libpulse-dev libgtk2.0-dev unzip git autoconf automake libtool
    git clone "$REPO_URL"
    cd "$REPO_DIR/src"
    ./autogen.sh
    ./configure
    make -j
    cd ..
    echo "DECtalk built for WSL.  Binaries are in dectalk/dist/"
else
    echo "Unsupported OS. For native Windows, use Visual Studio to build the solution manually."
    exit 1
fi
