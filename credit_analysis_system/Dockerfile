FROM python:3.9-slim

WORKDIR /app

# Install system dependencies needed for ReportLab and PDF processing
RUN apt-get update && apt-get install -y \
    build-essential \
    libfreetype6-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code (Now simpler structure)
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Command to run the dashboard
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]
