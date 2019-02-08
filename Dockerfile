FROM python:3.6-alpine

# set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy entrypoint to accessible location
COPY docker-entrypoint.sh /usr/local/bin/
RUN ["chmod", "+x", "/usr/local/bin/docker-entrypoint.sh"]

# Install Dependencies
RUN apk add --no-cache build-base libjpeg-turbo-dev postgresql-dev zlib-dev
RUN pip install --upgrade pip pipenv

# Copy application
WORKDIR /opt/km-api
COPY . /opt/km-api

# Install Third Party Packages
RUN pipenv install --ignore-pipfile --system

# Entrypoints into application
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
CMD ["server", "--bind", "0.0.0.0:8000"]
