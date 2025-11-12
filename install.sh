#!/bin/bash
set -e
echo "Installing Grok Direct P2P v0.2.1"
python3 -m venv venv
source venv/bin/activate
pip install "qrcode[pil]" pillow
echo "Done! Run: source venv/bin/activate && python node/grok_node.py"
