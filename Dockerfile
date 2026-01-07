FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    ENVIRONMENT=production

RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    git \
    curl \
    vim \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /src

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN groupadd -r appuser && useradd -r -g appuser appuser \
    && chown -R appuser:appuser /src

RUN chmod +x /src/entrypoint.sh

RUN if [ "$ENVIRONMENT" = "production" ]; then chown -R appuser:appuser /src; fi

USER root

CMD ["sh", "entrypoint.sh"]
