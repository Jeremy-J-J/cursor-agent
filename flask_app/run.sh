#!/bin/bash

# Simple script to run the Flask application
cd flask_app
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py