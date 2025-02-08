FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create data directory and copy questions.csv
RUN mkdir -p /data
COPY data/questions.csv /data/questions.csv

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_SERVER_LOG_LEVEL=debug
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Expose the port Streamlit runs on
EXPOSE 8501

# Command to run the application
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
