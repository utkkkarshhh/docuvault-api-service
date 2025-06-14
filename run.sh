#!/bin/bash

# Prevent Python from creating .pyc files and __pycache__ folders
export PYTHONDONTWRITEBYTECODE=1

# Run Django development server
python manage.py runserver 9000
