FROM python:3.11-alpine

# Install dependencies needed to build some packages
RUN apk add --no-cache gcc musl-dev libffi-dev

# Set working directory
WORKDIR /app

# Copy requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app's code
COPY . .

# Expose the port Flask will run on
EXPOSE 5000

# Start the Flask app (change `main` to your actual file name if different)
CMD ["python", "main.py"]
