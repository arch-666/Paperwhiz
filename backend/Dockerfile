# =========================
# 1. Builder Stage
# =========================
FROM python:3.11-slim AS builder

# Install system deps required for building Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl build-essential libssl-dev libffi-dev git \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry via official installer
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Disable venvs inside Docker
ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

WORKDIR /app

# Copy only dependency files for caching
COPY pyproject.toml poetry.lock* /app/

# Install dependencies (system packages built here)
RUN poetry install 

# Copy the rest of the backend code
COPY . /app


# =========================
# 2. Runtime Stage (final image)
# =========================
FROM python:3.11-slim

# Install runtime-only deps (no compilers)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libssl-dev libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy Poetry from builder
COPY --from=builder /root/.local /root/.local
ENV PATH="/root/.local/bin:$PATH"

# Copy installed packages and app from builder
COPY --from=builder /app /app
WORKDIR /app

# Env for Poetry
ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
