# base image
FROM python:3.12-slim-bookworm AS base

WORKDIR /app/api

# Install Poetry
ENV POETRY_VERSION=1.8.3
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --upgrade poetry==${POETRY_VERSION}

# Configure Poetry
ENV POETRY_CACHE_DIR=/tmp/poetry_cache
ENV POETRY_NO_INTERACTION=1
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV POETRY_VIRTUALENVS_CREATE=true

FROM base AS packages

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc g++ libc-dev libffi-dev libgmp-dev libmpfr-dev libmpc-dev

# Install Python dependencies
COPY pyproject.toml poetry.lock ./
RUN poetry install --sync --no-cache --no-root
# production stage
FROM base AS production

#ENV FLASK_APP=app.py
#ENV EDITION=SELF_HOSTED
#ENV DEPLOY_ENV=PRODUCTION
#ENV CONSOLE_API_URL=http://127.0.0.1:5001
#ENV CONSOLE_WEB_URL=http://127.0.0.1:3000
#ENV SERVICE_API_URL=http://127.0.0.1:5001
#ENV APP_WEB_URL=http://127.0.0.1:3000

EXPOSE 5001

# set timezone
ENV TZ=UTC

WORKDIR /app/api

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl wget vim nodejs ffmpeg libgmp-dev libmpfr-dev libmpc-dev \
    && apt-get autoremove \
    && rm -rf /var/lib/apt/lists/*

# Copy Python environment and packages
ENV VIRTUAL_ENV=/app/api/.venv
COPY --from=packages ${VIRTUAL_ENV} ${VIRTUAL_ENV}
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

# Copy source code
COPY . /app/api/

CMD ["python", "app.py"]

