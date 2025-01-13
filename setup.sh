#!/bin/bash

# Activate the virtual environment
source venv/bin/activate

# Upgrade pip to the latest version
pip install --upgrade pip

# Install project dependencies
pip install fastapi uvicorn jinja2 python-multipart pandas

# Optional: Save dependencies to requirements.txt
pip freeze > requirements.txt

echo "Virtual environment setup complete. Activate it with 'source venv/bin/activate'"
