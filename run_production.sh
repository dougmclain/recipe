#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Collect static files (optional, but good for production if we were using Nginx to serve them)
# python manage.py collectstatic --noinput

# Run Gunicorn
# -w 4: Use 4 worker processes
# -b 0.0.0.0:8000: Bind to all network interfaces on port 8000
# --access-logfile -: Log access to stdout
echo "Starting Recipe Server on port 8000..."
gunicorn recipe_project.wsgi:application -w 4 -b 0.0.0.0:8000 --access-logfile -
