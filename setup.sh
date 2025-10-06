#!/bin/bash

VENV_DIR="./venv"

# --- Cleanup ---
if [ -d "$VENV_DIR" ]; then
    rm -rf "$VENV_DIR"
    echo "Removed existing '$VENV_DIR' directory."
fi

# --- Create virtual environment ---
echo "Creating virtual environment '$VENV_DIR'..."
python3.11 -m venv "$VENV_DIR"

# --- Install requirements ---
echo "Upgrading pip and installing requirements..."
"$VENV_DIR/bin/python" -m pip install --upgrade pip setuptools
"$VENV_DIR/bin/python" -m pip install -r requirements.txt
echo "Setup Almost done."

# --- Setup API keys ---
# Print API key instructions in a single, multi-line echo
cat << EOF
Please visit https://admin.mistral.ai/organization/api-keys to obtain your API key.
Once you have your API key, create an .env file in app/ folder.
Set your API key as follows: MITRAL_API_KEY=<your_api_key_here>
If you do not set this, the application will not work.
Once done, you can start the application using ./start.sh'
EOF

