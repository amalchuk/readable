FROM python:3.9.5-buster
LABEL maintainer="Andrew Malchuk <andrew.malchuk@yandex.ru>" version="0.9.2"

WORKDIR /application
COPY ["requirements/production.txt", "/application/requirements.txt"]

ENV PIP_TIMEOUT="300" PIP_NO_CACHE_DIR="1" PIP_DISABLE_PIP_VERSION_CHECK="1"
RUN ["pip", "install", "--requirement", "requirements.txt", "--no-deps"]

COPY ["scripts/docker-entrypoint", "scripts/docker-healthcheck", "/usr/local/bin/"]
COPY ["scripts/uwsgi.xml", "manage.py", "/application/"]
COPY ["readable", "/application/readable/"]

HEALTHCHECK --interval=30s --timeout=5s --retries=1 CMD ["docker-healthcheck"]

EXPOSE 8000/tcp
ENTRYPOINT ["docker-entrypoint"]
CMD ["uwsgi", "uwsgi.xml"]
