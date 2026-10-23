# syntax=docker/dockerfile:1

FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=2.4.1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

RUN pip install --no-cache-dir "poetry==${POETRY_VERSION}"

WORKDIR /app

FROM base AS builder

COPY pyproject.toml poetry.lock ./
RUN poetry install --only main --no-root --no-ansi

COPY src ./src
RUN poetry install --only main --no-ansi

# Keep this stage before `runtime`: Docker builds the last stage by default and
# Render must never build the dev image (uvicorn --reload).
FROM base AS dev

ENV PATH="/app/.venv/bin:${PATH}"

RUN groupadd --system app && useradd --system --gid app --home-dir /app app

COPY pyproject.toml poetry.lock ./
RUN poetry install --with dev --no-root --no-ansi

COPY --chown=app:app . .
RUN poetry install --with dev --no-ansi && chown app:app /app

USER app

EXPOSE 8000

CMD ["uvicorn", "tricolink.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--limit-concurrency", "200"]

FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000 \
    PATH="/app/.venv/bin:${PATH}"

RUN groupadd --system app && useradd --system --gid app --home-dir /app app

WORKDIR /app

COPY --from=builder --chown=app:app /app/.venv /app/.venv
COPY --from=builder --chown=app:app /app/src /app/src
COPY --chown=app:app alembic.ini /app/alembic.ini
COPY --chown=app:app alembic /app/alembic

USER app

EXPOSE 8000

# Render injects PORT (default 10000); bind to it instead of the hardcoded 8000.
# Gunicorn 26 defaults its control socket to $HOME/.gunicorn, which the
# unprivileged `app` user cannot create under /app; we do not use it.
CMD ["sh", "-c", "exec gunicorn tricolink.main:app --worker-class uvicorn.workers.UvicornWorker --workers ${WEB_CONCURRENCY:-2} --bind 0.0.0.0:${PORT:-8000} --no-control-socket --access-logfile - --error-logfile -"]
