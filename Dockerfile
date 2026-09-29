FROM python:3.12-slim

ARG APP_VERSION=1.0.0

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV APP_VERSION=${APP_VERSION}

WORKDIR /app

RUN groupadd --system appuser && useradd --system --gid appuser --create-home appuser

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY core ./core
COPY web ./web
COPY main.py .

RUN mkdir -p /app/web_workspace && chown -R appuser:appuser /app

USER appuser

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "--threads", "4", "--timeout", "120", "web.app:app"]
