# Use Python 3.12 slim image
FROM python:3.12-slim

# Install dependencies for ffmpeg (including ffmpeg binary)
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*  # Clean up unnecessary files to reduce image size

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files into the container
COPY . .

# Run the application
CMD ["python", "app.py"]