FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy project
COPY . /app/

# Create media directory
RUN mkdir -p /app/media && \
    chmod -R 755 /app/media

# Create static directory
RUN mkdir -p /app/static && \
    chmod -R 755 /app/static

# Expose port 8000
EXPOSE 8000

# Create entrypoint script
RUN echo '#!/bin/bash\n\
# Apply database migrations\n\
python manage.py migrate --noinput\n\
\n\
# Start the Django server\n\
python manage.py runserver 0.0.0.0:8000\n\
' > /app/entrypoint.sh && chmod +x /app/entrypoint.sh

# Run script
CMD ["/app/entrypoint.sh"]