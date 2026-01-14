# Multi-stage build for optimized image size
FROM python:3.8-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/
COPY config/ ./config/

# Create directories for data and models
RUN mkdir -p data/raw data/processed models reports/figures logs

# Training stage
FROM base as training
CMD ["python", "src/train.py"]

# Inference stage
FROM base as inference
COPY models/ ./models/
CMD ["python", "src/inference.py"]

# Default stage
FROM base as default
CMD ["python", "src/train.py"]
