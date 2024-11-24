# Use the official Python 3.11 image as the base image
FROM python:3.11.0-slim

# Set the working directory in the container
WORKDIR /app

# Install dependencies for building sqlite3, Tesseract, Poppler, and other required libraries
RUN apt-get update && \
    apt-get install -y wget build-essential libreadline-dev ffmpeg libsm6 libxext6 \
    poppler-utils tesseract-ocr && \
    rm -rf /var/lib/apt/lists/*

# Update the dynamic linker run-time bindings
RUN ldconfig

# Upgrade pip to the latest version
RUN python -m pip install --upgrade pip

# Copy only the requirements file to leverage Docker cache
COPY requirements.txt .

# Install any required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port your Flask app runs on
EXPOSE 5000

# Run the application
CMD ["python", "server.py"]
