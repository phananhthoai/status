FROM harbor.elofun.net/core/nginx-static:0.0.1

RUN apt update && \
    curl -sL https://deb.nodesource.com/setup_16.x | bash -


COPY . /var/www/
