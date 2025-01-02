# Use an official Python runtime as a parent image (Python 3.10)
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install the dependencies required by tkinter
RUN apt-get update && \
    apt-get install -y \
    libtk8.6 \
    && rm -rf /var/lib/apt/lists/*  # Clean up to reduce image size

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Run tests
RUN pytest

# Run main.py when the container launches
CMD ["python", "main.py"]
