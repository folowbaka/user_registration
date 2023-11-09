# Build image
FROM python:3.10-slim-buster as python-build
RUN useradd -m nonrootuser
ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_PATH=/home/nonrootuser/.local \
    VENV_PATH=/home/nonrootuser/venv \
    POETRY_VERSION=1.6.1
ENV PATH="$POETRY_PATH/bin:$VENV_PATH/bin:$PATH"
RUN apt-get update \
    && apt-get install -y \
    curl \
    gcc \
    libpq-dev
USER nonrootuser
    # install poetry - uses $POETRY_VERSION internally
RUN curl -sSL https://install.python-poetry.org | python3 - \
    # configure poetry & make a virtualenv ahead of time since we only need one
    && python -m venv $VENV_PATH \
    && python -m pip install --upgrade pip \
    && poetry config virtualenvs.create false
COPY poetry.lock pyproject.toml ./
RUN . $VENV_PATH/bin/activate \
    && poetry install --no-interaction --no-ansi --only main -vvv

# Runtime image
FROM python:3.10-slim-buster as runtime
RUN useradd -m nonrootuser
RUN apt-get update \
    && apt-get install -y \
    libpq-dev
ENV VENV_PATH=/home/nonrootuser/venv \
    PATH="/home/nonrootuser/venv/bin:$PATH" \
    PYTHONPATH=/app
WORKDIR /app
COPY --from=python-build --chown=nonrootuser:nonrootuser $VENV_PATH $VENV_PATH
COPY --chown=nonrootuser:nonrootuser . ./
EXPOSE 9000
USER nonrootuser
CMD gunicorn "asgi:app" -c gunicorn_conf.py