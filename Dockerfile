# Use Python slim image (includes pip and works with PaddleOCR)
FROM python:3.10-slim

# Install required system packages for OCR + OpenCV
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libgl1-mesa-glx \
    libsm6 \
    libxext6 \
    libxrender-dev \
    build-essential \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Set working directory inside container
WORKDIR /app

# Copy all files into container
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose Flask port
EXPOSE 5000

# Run your Flask app
CMD ["python", "app.py"]
