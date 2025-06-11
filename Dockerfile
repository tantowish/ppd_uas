FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install build tools and Python headers
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    libblas-dev \
    liblapack-dev \
    build-essential \
    python3-dev \
    bash \
 && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the Cloud Run port
EXPOSE 8080

# Run the app
CMD ["python", "main.py"]
