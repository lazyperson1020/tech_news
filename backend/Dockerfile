# Dockerfile for Django backend
# Use official Python slim image as base
FROM python:3.11-slim

# prevent Python from writing .pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set working directory
WORKDIR /app

# install system dependencies (if any)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# copy and install Python dependencies
COPY requirements.txt ./
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# copy project files
COPY . .

# collect static files (in case it's needed in production)
RUN python manage.py collectstatic --noinput || true

# expose port Django will run on
EXPOSE 8000

# default command using gunicorn
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
