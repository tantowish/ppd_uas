# Use official slim Python image (better compatibility than Alpine)
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Prevent pip root warning
ENV PIP_ROOT_USER_ACTION=ignore

# Install system build dependencies
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

# Copy requirements first (for caching)
COPY requirements.txt .

# Upgrade pip and setuptools
RUN pip install --upgrade pip setuptools wheel

# Rebuild numpy and pandas from source to avoid binary mismatch
RUN pip install --no-binary :all: numpy==1.23.5 pandas==1.5.2

# Install remaining packages
RUN pip install --no-cache-dir \
    flask==3.1.1 \
    flask_cors==6.0.0 \
    joblib==1.3.2 \
    pydantic==2.11.5 \
    requests==2.32.3 \
    streamlit==1.45.1

# Copy application code
COPY . .

# Expose Cloud Run default port
EXPOSE 8080

# Run your Flask app
CMD ["python", "main.py"]
