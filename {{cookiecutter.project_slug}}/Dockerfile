FROM cloudron/base:4.2.0@sha256:46da2fffb36353ef714f97ae8e962bd2c212ca091108d768ba473078319a47f4

ARG CLOUDRON_OIDC_CLIENT_ID
ARG CLOUDRON_OIDC_CLIENT_SECRET
ARG CLOUDRON_OIDC_ISSUER
ARG CLOUDRON_POSTGRESQL_DATABASE
ARG CLOUDRON_POSTGRESQL_USERNAME
ARG CLOUDRON_POSTGRESQL_PASSWORD
ARG CLOUDRON_POSTGRESQL_HOST
ARG CLOUDRON_POSTGRESQL_PORT
ARG CLOUDRON_REDIS_PASSWORD
ARG CLOUDRON_REDIS_HOST
ARG CLOUDRON_REDIS_PORT
ENV DEBUG=False
ENV RUST_BACKTRACE=full

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.10 \
    python3.10-dev \
    python3.10-venv \
    {% if cookiecutter.database == "postgresql" %}libpq-dev{% else %}default-libmysqlclient-dev{% endif %} build-essential \
    supervisor \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create and switch to a non-root user
RUN useradd --create-home django
WORKDIR /app/code

# Install uv
RUN pip install --no-cache-dir uv

# Create and activate virtual environment outside of /app/code so it is not overwritten by the docker-compose volume
ENV VIRTUAL_ENV=/app/.venv
RUN uv venv $VIRTUAL_ENV --python 3.10

# Add the virtual environment to the path
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Set Python 3.10 as default Python
RUN ln -s /usr/bin/python3.10 /usr/bin/python

# Install Python dependencies using uv
COPY --chown=django:django ./pyproject.toml ./
RUN uv pip install -r <(uv pip compile pyproject.toml)

# Copy project files
COPY --chown=django:django . .

# Copy configuration files
COPY --chown=django:django ./supervisor/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY --chown=django:django ./compose/django/entrypoint /entrypoint
COPY --chown=django:django ./compose/django/start.asgi /start
COPY --chown=django:django ./compose/django/celery-hooks /celery-hooks

# Make scripts executable
RUN chmod +x /entrypoint /start /celery-hooks

# Create required directories
RUN mkdir -p /app/data/media /app/data/static /app/data/log/supervisor /app/data/run

# Set environment variables
ENV DJANGO_SETTINGS_MODULE={{ cookiecutter.project_slug }}.settings
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/code:${PATH}"
ENV UV_HTTP_TIMEOUT=1200

# Change ownership of data directories
RUN chown -R django:django /app/data

ENTRYPOINT ["/entrypoint"]
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]

EXPOSE 8000