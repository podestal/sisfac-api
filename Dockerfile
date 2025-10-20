# # Use Python 3.13 slim image
# FROM python:3.13-slim

# # Set environment variables
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1

# # Set work directory
# WORKDIR /app

# # Install system dependencies
# RUN apt-get update \
#     && apt-get install -y --no-install-recommends \
#         postgresql-client \
#         build-essential \
#         libpq-dev \
#     && rm -rf /var/lib/apt/lists/*

# # Install Python dependencies
# COPY requirements.txt /app/
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy project
# COPY . /app/

# # Create entrypoint script
# COPY docker-entrypoint.sh /app/
# RUN chmod +x /app/docker-entrypoint.sh

# # Expose port
# EXPOSE 8000

# # Run entrypoint script
# ENTRYPOINT ["/app/docker-entrypoint.sh"]

# FROM python:3.11-bookworm

# ENV PYTHONUNBUFFERED=1

# # Ensure /tmp directory exists and is writable
# RUN mkdir -p /tmp && chmod 1777 /tmp

# COPY ./requirements.txt /tmp/requirements.txt
# COPY ./scripts /scripts
# COPY ./app /app

# WORKDIR /app
# EXPOSE 8000
# ARG DEV=false

# RUN python -m venv /py && \
#     /py/bin/pip install --upgrade pip && \
#     apt-get update && \
#     apt-get install -y --no-install-recommends sudo postgresql-client libjpeg-dev && \
#     apt-get install -y --no-install-recommends build-essential libpq-dev zlib1g-dev && \
#     /py/bin/pip install -r /tmp/requirements.txt && \
#     if [ $DEV = "true" ]; then /py/bin/pip install -r /tmp/requirements.dev.txt ; fi && \
#     apt-get purge -y --auto-remove build-essential && \
#     apt-get clean && \
#     rm -rf /var/lib/apt/lists/* && \
#     adduser \
#     --disabled-password \
#     --gecos "" \
#     --home /home/django-user \
#     django-user && \
#     usermod -aG sudo django-user && \
#     echo "django-user ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && \
#     mkdir -p /vol/web/media && \
#     mkdir -p /vol/web/static && \
#     chown -R django-user:django-user /vol /home/django-user && \
#     chmod -R 777 /vol && \
#     chmod -R +x /scripts && \
#     rm -rf /tmp  # Move tmp cleanup to the end

# ENV PATH="/scripts:/py/bin:$PATH"

# USER django-user

# CMD ["run.sh"]

FROM python:3.11-bookworm

ENV PYTHONUNBUFFERED=1

# Ensure /tmp directory exists and is writable
RUN mkdir -p /tmp && chmod 1777 /tmp

COPY ./requirements.txt /tmp/requirements.txt
COPY ./scripts /scripts
COPY ./app /app

# COPY ./app/sisfac/staticfiles /vol/web/static/

WORKDIR /app
EXPOSE 8000
ARG DEV=false

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apt-get update && \
    apt-get install -y --no-install-recommends sudo postgresql-client libjpeg-dev && \
    apt-get install -y --no-install-recommends build-essential libpq-dev zlib1g-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; then /py/bin/pip install -r /tmp/requirements.dev.txt ; fi && \
    apt-get purge -y --auto-remove build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    adduser \
    --disabled-password \
    --gecos "" \
    --home /home/django-user \
    django-user && \
    usermod -aG sudo django-user && \
    echo "django-user ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && \
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    chown -R django-user:django-user /vol /home/django-user && \
    chmod -R 755 /vol/web/static && \
    chmod -R 777 /vol/web/media && \
    chmod -R +x /scripts && \
    rm -rf /tmp  # Move tmp cleanup to the end

ENV PATH="/scripts:/py/bin:$PATH"

USER django-user

CMD ["run.sh"]
