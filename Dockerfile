# Use the official Python base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements.txt first for efficient Docker layer caching
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the working directory
COPY app.py /app/

# Expose the Flask app port
EXPOSE 8080

# Run the Flask application
CMD ["python", "app.py"]
