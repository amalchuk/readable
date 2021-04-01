FROM python:3.9.2-buster
LABEL maintainer="Andrew Malchuk <andrew.malchuk@yandex.ru>" version="0.6.7"

WORKDIR /application
COPY ["scripts/docker-entrypoint", "scripts/docker-healthcheck", "/usr/local/bin/"]
COPY ["scripts/uwsgi.xml", "manage.py", "/application/"]
COPY ["requirements/production.txt", "/application/requirements.txt"]
COPY ["readable", "/application/readable/"]

ENV PIP_NO_CACHE_DIR="1" PIP_DISABLE_PIP_VERSION_CHECK="1"
RUN ["pip", "install", "--requirement", "requirements.txt", "--no-deps", "--quiet"]

HEALTHCHECK --interval=30s --timeout=5s CMD ["docker-healthcheck"]

EXPOSE 8000-8003/tcp
ENTRYPOINT ["docker-entrypoint"]
CMD ["uwsgi", "uwsgi.xml"]
