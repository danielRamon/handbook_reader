# Use Python slim-buster as base image for smaller size
FROM python:3.10.15-slim

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy Python source files
COPY *.py .

# Start Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port", "2000"]

