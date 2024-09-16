# Use a minimal Python image with production capabilities
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY src/* ./
COPY templates/ templates/

# Expose the port the app runs on
EXPOSE 5000

# Set environment variables for production
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Run the application using gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
