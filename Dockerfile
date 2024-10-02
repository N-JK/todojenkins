# Use official Python slim base image
FROM python:3.12-slim

# Set environment variables to avoid bytecode creation and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /usr/src/app

# Install system dependencies for PostgreSQL and any other necessary packages
RUN apt-get update && apt-get install -y libpq-dev gcc

# Install Python dependencies (including pytest for testing)
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

# Install pytest (added to support testing)
RUN pip install pytest

# Copy the application code into the container
COPY . /usr/src/app/

# Collect static files for production
RUN python manage.py collectstatic --noinput

# Expose the port for the Gunicorn server (optional but recommended)
EXPOSE 8000

# Command to run the Django application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "todo_list.wsgi:application"]
