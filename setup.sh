#!/bin/bash

command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# install vlc and yt-dlp
if ! command_exists vlc; then
    echo "Installing VLC..."
    apt update && apt install -y vlc
else
    echo "VLC is already installed."
fi

# Install yt-dlp if it's not installed
if ! command_exists yt-dlp; then
    echo "Installing yt-dlp..."
    python3 -m pip install --upgrade yt-dlp
else
    echo "yt-dlp is already installed."
fi

# path for the script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ALIAS_NAME="tlofi"

# create alias
if ! grep -q "alias $ALIAS_NAME=" ~/.bashrc; then
    echo "Creating alias for tlofi..."
    echo "alias $ALIAS_NAME='python3 $SCRIPT_DIR/tlofi.py'" >> ~/.bashrc
    echo "Alias created. Restart your terminal or run 'source ~/.bashrc' to use it."
fi

echo "Setup complete!"