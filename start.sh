#!/bin/bash
# Grok Direct P2P — One-Click Start

echo "Starting Grok P2P..."

# Install deps
python3 -m pip install --user -r requirements.txt

# Start ngrok
ngrok http 8000 --url=taylor-music.ngrok.io &

# Wait 5s
sleep 5

# Start node
cd relay
python3 node/grok_node.py
