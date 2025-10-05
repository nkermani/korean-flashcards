#!/bin/bash
# --- Create virtual environment ---
echo "Creating virtual environment 'venv'..."
python3.11 -m venv venv

# --- Activate virtual environment ---
source venv/bin/activate

# --- Upgrade pip and setuptools ---
echo "Upgrading pip and setuptools..."
pip install --upgrade pip setuptools

# --- Install requirements ---
echo "Installing packages from requirements.txt..."
pip install -r requirements.txt
