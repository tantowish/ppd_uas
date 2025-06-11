# Use Python 3.10 slim image (binary-compatible)
FROM python:3.10-slim

WORKDIR /app

ENV PIP_ROOT_USER_ACTION=ignore

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libffi-dev \
    libblas-dev \
    liblapack-dev \
    build-essential \
    python3-dev \
    bash \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and setuptools
RUN pip install --upgrade pip setuptools wheel

# Copy and install requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy app code
COPY . .

# Expose port for Cloud Run
EXPOSE 8080

# Run the app
CMD ["python", "main.py"]
