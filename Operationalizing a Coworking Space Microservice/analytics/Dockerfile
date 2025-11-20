FROM public.ecr.aws/docker/library/python:3.8-slim

WORKDIR /app

# Update package list and install system dependencies required for PostgreSQL
# build-essential: Compilers and build tools needed for Python packages with C extensions
# libpq-dev: PostgreSQL development libraries required by psycopg2
RUN apt update -y && \
    apt install -y build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements file first to leverage Docker cache
COPY requirements.txt .

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the application port
EXPOSE 5153

# Run the Flask application
CMD ["python", "app.py"]

