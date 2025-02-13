#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status.

# Create a Python virtual environment in /app/venv
python -m venv /app/venv

# Path to the virtual environment
VENV_PATH="/app/venv"

# Activate the virtual environment
source $VENV_PATH/bin/activate

# Upgrade pip to the latest version
pip install --upgrade pip

# Install Django and Django REST framework
pip install django djangorestframework

# Install psycopg2 for PostgreSQL database
pip install psycopg2

# Path to the Django project directory
PROJECT_DIR=/app/comparators

# Check if the Django project already exists
if [ ! -f "$PROJECT_DIR/manage.py" ]; then
    echo "Django project does not exist, creating project..."
    cd /app
    django-admin startproject comparators

    # Move into the project directory
    cd $PROJECT_DIR

    # Create a new Django app named 'core'
    python manage.py startapp core
fi

# Execute the following commands (e.g., Django migrations)
cd $PROJECT_DIR
echo "Running migrations..."
python manage.py migrate

# Start the Django server
echo "Starting the Django server..."
exec python manage.py runserver 0.0.0.0:9000