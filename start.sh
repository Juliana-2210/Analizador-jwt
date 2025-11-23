#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Run gunicorn
gunicorn --bind 0.0.0.0:5000 --workers 4 --worker-class sync --timeout 60 app:app
