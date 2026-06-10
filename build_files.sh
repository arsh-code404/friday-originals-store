#!/bin/bash
echo "=== Start Friday Originals Store Build ==="

# Install dependencies using the system packages override since the build container is disposable
python3 -m pip install -r requirements.txt --break-system-packages

# Collect static files
python3 manage.py collectstatic --noinput --clear

echo "=== End Friday Originals Store Build ==="
