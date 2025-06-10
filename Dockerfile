FROM python:3.11-alpine

# Install build dependencies
RUN apk add --no-cache gcc musl-dev libffi-dev

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port 8080 (required by Cloud Run)
EXPOSE 8080

# Set environment variable for Flask to find the app (if needed)
# ENV FLASK_APP=main.py

# Start the Flask app on port 8080 and all interfaces
CMD ["python", "main.py"]