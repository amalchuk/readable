FROM python:3.9.1-buster
LABEL maintainer="Andrew Malchuk <andrew.malchuk@yandex.ru>" version="0.5.3"

WORKDIR /application
COPY --chown=nobody:nogroup ["deployment/readable/docker-entrypoint", "/usr/local/bin/"]
COPY --chown=nobody:nogroup ["deployment/readable/uwsgi.xml", "manage.py", "/application/"]
COPY --chown=nobody:nogroup ["requirements/production.txt", "/application/requirements.txt"]
COPY --chown=nobody:nogroup ["readable", "/application/readable/"]

ENV PIP_NO_CACHE_DIR="1" PIP_DISABLE_PIP_VERSION_CHECK="1"
RUN ["python", "-m", "pip", "install", "--requirement", "requirements.txt", "--no-deps", "--quiet"]

EXPOSE 8000-8003/tcp
ENTRYPOINT ["docker-entrypoint"]
CMD ["uwsgi", "uwsgi.xml"]
