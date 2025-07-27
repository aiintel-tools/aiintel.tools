#!/bin/bash

# Create uploads directory if it doesn't exist
mkdir -p uploads/tool_images

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check if database exists
if [ ! -f "instance/ai_directory.db" ]; then
    echo "Initializing database..."
    python seed.py --reset
else
    echo "Database already exists."
fi

# Run the application
echo "Starting server..."
gunicorn -c gunicorn_config.py app:app

