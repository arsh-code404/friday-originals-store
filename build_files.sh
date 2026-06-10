#!/bin/bash
echo "=== Start Friday Originals Store Build ==="

# Create and activate a virtual environment for the build phase
python3 -m venv venv
source venv/bin/activate

# Install dependencies in the isolated virtual environment
python3 -m pip install -r requirements.txt

# Collect static files
python3 manage.py collectstatic --noinput --clear

echo "=== End Friday Originals Store Build ==="
