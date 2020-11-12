FROM python:3.9-buster
LABEL maintainer="Andrew Malchuk <andrew.malchuk@yandex.ru>" version="0.1.5.1"

WORKDIR /application
COPY ["deployment/readable/docker-entrypoint", "/usr/local/bin/"]
COPY ["deployment/readable/uwsgi.xml", "manage.py", "/application/"]
COPY ["requirements/production.txt", "/application/requirements.txt"]
COPY ["readable", "/application/readable/"]

ENV PIP_NO_CACHE_DIR="1" PIP_DISABLE_PIP_VERSION_CHECK="1" UWSGI_XML="/application/uwsgi.xml"
RUN ["pip", "install", "--requirement", "requirements.txt", "--no-deps", "--require-hashes"]

# Explicitly set user/group IDs:
RUN ["groupadd", "--system", "--gid", "666", "uwsgi"]
RUN ["useradd", "--system", "--gid", "uwsgi", "--uid", "666", "--home-dir", "/application", "--shell", "/bin/bash", "uwsgi"]
RUN ["chown", "--recursive", "uwsgi:uwsgi", "/application"]
USER uwsgi

EXPOSE 8000-8003/tcp
ENTRYPOINT ["docker-entrypoint"]
CMD ["uwsgi"]
