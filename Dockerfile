FROM python:3.10-alpine

# Install system build dependencies
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    g++ \
    libc-dev \
    linux-headers \
    openblas-dev \
    freetype-dev \
    lapack-dev \
    python3-dev \
    build-base \
    py3-pip \
    bash

# Set working directory
WORKDIR /app

# Copy requirements first and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port 8080 (required by Cloud Run)
EXPOSE 8080

# Command to run the app
CMD ["python", "main.py"]
