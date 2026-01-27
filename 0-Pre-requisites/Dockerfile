# Use Python base image
FROM python:3.8-slim
FROM rabbitmq:3-management

# Set the working directory inside the container
WORKDIR /app
COPY hello_from_volume.py /app/hello_from_volume.py
# Command to run a script from the volume (this script will be provided by the volume)
CMD ["python", "/app/hello_from_volume.py"]
