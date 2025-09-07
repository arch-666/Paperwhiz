# =========================
# 1. Builder Stage
# =========================
FROM python:3.11-slim-bookworm AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libssl-dev libffi-dev curl git \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry via pipx or official installer
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

# Copy only dependency files for caching
COPY pyproject.toml poetry.lock* /app/

# Create a virtualenv and install dependencies
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

RUN poetry install --no-root --without dev


# Copy application code
COPY . /app

# =========================
# 2. Runtime Stage
# =========================
FROM python:3.11-slim-bookworm

# Install minimal runtime libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    libssl3 libffi8 \
    && rm -rf /var/lib/apt/lists/*

# Copy venv and app from builder
COPY --from=builder /venv /venv
COPY --from=builder /app /app

ENV PATH="/venv/bin:$PATH"
WORKDIR /app

EXPOSE 8000

# Directly run uvicorn from venv
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

