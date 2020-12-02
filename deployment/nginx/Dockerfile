FROM nginx:mainline-alpine
LABEL maintainer="Andrew Malchuk <andrew.malchuk@yandex.ru>" version="0.2.0"

WORKDIR /etc/nginx
COPY ["docker-entrypoint", "/usr/local/bin/"]
COPY ["mime.types", "nginx.conf", "uwsgi_params", "/etc/nginx/"]

ENTRYPOINT ["docker-entrypoint"]
CMD ["nginx"]
