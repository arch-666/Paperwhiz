FROM python:3.11-slim

# Install Poetry
RUN pip install poetry

WORKDIR /app

# Copy dependency files first (better caching)
COPY pyproject.toml poetry.lock* /app/

# Install dependencies (without dev in Docker)
RUN poetry install --no-root --no-dev

# Copy the rest of the backend code
COPY . /app

# Start FastAPI with Uvicorn
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
