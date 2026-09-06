# ==============================================================================
# Build Stage: Install dependencies using uv
# ==============================================================================
FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

# Install dependencies in a cached layer before copying application code
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-install-project

# Copy the full application code
COPY . .

# Sync project package
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# ==============================================================================
# Final Runtime Stage: Minimal production image
# ==============================================================================
FROM python:3.14-slim-bookworm

WORKDIR /app

# Create a non-privileged user for container security
RUN addgroup --system app && adduser --system --group app

# Copy virtual environment and project code from builder
COPY --from=builder --chown=app:app /app /app

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

USER app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
