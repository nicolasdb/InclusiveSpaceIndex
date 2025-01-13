FROM python:3.9-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Create necessary directories if they don't exist
RUN mkdir -p static templates

# Expose the port the app runs on
EXPOSE 7860

# Set environment variables
ENV PYTHONPATH=/app
ENV SMTP_HOST=${SMTP_HOST}
ENV SMTP_PORT=${SMTP_PORT}
ENV SMTP_USER=${SMTP_USER}
ENV SMTP_PASS=${SMTP_PASS}

# Command to run the application
CMD ["python", "app.py"]
