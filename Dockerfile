FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install deps in a separate layer for Docker cache efficiency
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source (frontend/ and .venv/ are excluded via .dockerignore)
COPY app/ app/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
