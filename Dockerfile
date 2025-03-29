FROM python:3.10-slim

# Install OS-level dependencies (libGL for OpenCV, etc.)
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy everything into the container
COPY . .

# Create venv & install Python dependencies
RUN python -m venv venv && \
    . venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

# Expose port
EXPOSE 8000

# Start the app
CMD [ "venv/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000" ]
