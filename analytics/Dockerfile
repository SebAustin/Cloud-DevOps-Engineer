FROM python:3.8-slim

# Set working directory
WORKDIR /app

# Update package index and install system dependencies required for building Python packages
# build-essential: provides gcc and other tools needed to compile Python extensions
# libpq-dev: PostgreSQL client library headers needed for psycopg2
RUN apt update -y && \
    apt install -y build-essential libpq-dev && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip, setuptools, and wheel to ensure compatibility with modern Python packages
RUN pip install --upgrade pip setuptools wheel

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the application port
EXPOSE 5153

# Run the application
CMD ["python", "app.py"]

