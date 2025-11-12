#!/bin/bash
set -e
echo "🚀 Installing Grok Direct P2P v0.2.1 – Original (rough demo) Edition"
python3 -m venv venv
source venv/bin/activate
pip install qrcode[pil] pillow
echo "✅ Done! Run with: source venv/bin/activate && python node/grok_node.py"
echo "First track already in library: Original (rough demo) by Taylor Dolletzki"
