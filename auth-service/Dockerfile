FROM python:3.12-slim

WORKDIR /app

# Install system dependencies (needed for compilation of some python packages)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Command is overridden in docker-compose, but good to have default
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
