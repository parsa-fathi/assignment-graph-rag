# Use the official Python image from the Docker Hub
FROM python:3.12.2-slim-bullseye

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    poppler-utils \
    tesseract-ocr \
    tesseract-ocr-eng \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r /app/requirements.txt && rm -rf ~/.cache/pip

# Make port 80 and 6379 available to the world outside this container
EXPOSE 80 6379

# Define environment variable
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python", "/app/src/main.py", "--host=0.0.0.0"]