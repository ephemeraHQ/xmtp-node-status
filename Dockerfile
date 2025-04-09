# Use an official lightweight Python image as base
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements first to leverage Docker caching
COPY requirements.txt /app/requirements.txt

# Install dependencies before copying the script
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY NodeRegistry.abi.json /app/NodeRegistry.abi.json

# Copy the actual script last (ensures that if only the script changes, the previous layers are cached)
COPY grpc_status_server.py /app/grpc_status_server.py

# Expose the port the server runs on
EXPOSE 5000

# Command to run the application
CMD ["python", "/app/grpc_status_server.py"]