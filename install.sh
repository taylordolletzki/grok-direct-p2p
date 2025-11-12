
6. Scroll down → commit message:  
   `v0.2.1 – clean naming, $0.0333 default price`  
7. Click **Commit changes** (green button).

### Step 2: Replace install.sh
1. Click **install.sh** in the root.  
2. Click the **pencil icon ✏️** → “Edit this file”.  
3. **Select ALL** → **Delete**.  
4. Paste this **exact version**:

```bash
#!/bin/bash
set -e
echo "Installing Grok Direct P2P v0.2.1"
python3 -m venv venv
source venv/bin/activate
pip install "qrcode[pil]" pillow
echo "Done! Run: source venv/bin/activate && python node/grok_node.py"
