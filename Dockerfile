# Use an official Python runtime as a base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=development
ENV PORT=5002

# Expose the port the app runs on
EXPOSE 5002

# Run the application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5002"]
