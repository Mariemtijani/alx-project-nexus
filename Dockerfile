FROM python:3.11-slim

# Install PostgreSQL client dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Django project files (mounted later via volume)
COPY ./app /app

# Expose port 8000
EXPOSE 8000

CMD ["bash","-lc","cd /app/app && python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn core.wsgi:application --bind 0.0.0.0:$PORT"]


