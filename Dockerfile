# Dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# System deps (add build tools if needed by psycopg or others)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl && \
    rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static at build time (no DB needed)
# Make sure settings.py has STATIC_ROOT set!
RUN python manage.py collectstatic --noinput

# Render sets $PORT automatically.
# Run migrations on boot, then start gunicorn
CMD bash -lc "python manage.py migrate && gunicorn core.wsgi:application --bind 0.0.0.0:$PORT"
