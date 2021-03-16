FROM python:3.9.2-buster
LABEL maintainer="Andrew Malchuk <andrew.malchuk@yandex.ru>" version="0.6.3"

WORKDIR /application
COPY --chown=nobody:nogroup ["scripts/docker-entrypoint", "/usr/local/bin/"]
COPY --chown=nobody:nogroup ["scripts/uwsgi.xml", "manage.py", "/application/"]
COPY --chown=nobody:nogroup ["requirements/production.txt", "/application/requirements.txt"]
COPY --chown=nobody:nogroup ["readable", "/application/readable/"]

ENV PIP_NO_CACHE_DIR="1" PIP_DISABLE_PIP_VERSION_CHECK="1"
RUN ["pip", "install", "--requirement", "requirements.txt", "--no-deps", "--quiet"]

VOLUME ["/application/readable/resources/mediafiles", "/application/readable/resources/staticfiles"]

EXPOSE 8000-8003/tcp
ENTRYPOINT ["docker-entrypoint"]
CMD ["uwsgi", "uwsgi.xml"]
