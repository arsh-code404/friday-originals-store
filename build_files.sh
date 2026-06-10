#!/bin/bash
echo "=== Start Friday Originals Store Build ==="
python3 -m pip install -r requirements.txt
python3 manage.py collectstatic --noinput --clear
echo "=== End Friday Originals Store Build ==="
