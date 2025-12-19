#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Python dependencies
pip install -r ats-checker/requirements.txt

# Collect static files
cd ats-checker/core
python manage.py collectstatic --no-input
python manage.py migrate

# Install frontend dependencies and build
cd ../../frontend
npm install
npm run build
