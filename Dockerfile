FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    DJANGO_SETTINGS_MODULE=customer_management.settings.prod

RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home appuser

COPY requirements/base.txt requirements/base.txt
RUN pip install -r requirements/base.txt

COPY . .

RUN mkdir -p /app/staticfiles /app/media && chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

CMD ["gunicorn", "customer_management.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
