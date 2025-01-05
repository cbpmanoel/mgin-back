# Use the official Ubuntu 22.04 as the base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the application
COPY src/ ./src/
COPY app.py .
COPY fastapi_metadata.py .

# Copy the resources/images folder and its contents
COPY resources/images /app/resources/images

# Set the entrypoint to run the application with Python optimizations
ENTRYPOINT ["python3", "-OO", "app.py"]