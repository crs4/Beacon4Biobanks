##########################
## Build env
##########################

FROM python:3.10-buster AS BUILD

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
#RUN apt-get upgrade -y
RUN apt-get install -y --no-install-recommends \
    ca-certificates pkg-config make \
    libssl-dev libffi-dev libpq-dev

# python packages
RUN pip install --upgrade pip
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt


##########################
## Final image
##########################
FROM python:3.10-buster

ARG UID=1000
ARG GID=1000

LABEL maintainer "CRS4"
LABEL org.label-schema.schema-version="2.0"
LABEL org.label-schema.vcs-url="https://github.com/CRS4/Beacon4Biboanks/"

# Too much ?
COPY --from=BUILD /usr/local/bin      /usr/local/bin
COPY --from=BUILD /usr/local/lib      /usr/local/lib

RUN apt-get update && \
#    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    nginx gettext-base \
    && \
    rm -rf /var/lib/apt/lists/* /etc/apt/sources.list.d/nginx.list && \
    apt-get purge -y --auto-remove

RUN pip install supervisor
ENV SSL_KEY_FILE=/beacon/nginx/certs/beacon.key
ENV SSL_CERT_FILE=/beacon/nginx/certs/beacon.cert

RUN mkdir -p /beacon/nginx/service
RUN mkdir -p /beacon/nginx/certs

COPY docker/conf/nginx.conf          /beacon/nginx/nginx.conf
COPY docker/conf/*.template          /beacon/nginx/service/
COPY docker/conf/supervisord.conf    /beacon/supervisord.conf
COPY docker/conf/entrypoint.sh       /usr/local/bin/entrypoint.sh
COPY beacon/                         /beacon/beacon

RUN groupadd -g $GID beacon                      && \
    useradd -u $UID -M -g beacon beacon          && \
    mkdir /var/run/beacon                        && \
    chown -R beacon:beacon /beacon               && \
    chown -R beacon:beacon /var/log/nginx        && \
    chown -R beacon:beacon /var/lib/nginx        && \
    chown -R beacon:beacon /etc/nginx            && \
    chown -R beacon:beacon /var/run/beacon       && \
    mkdir -p /var/log/supervisord                && \
    chown -R beacon:beacon /var/log/supervisord  && \
    chmod +x /usr/local/bin/entrypoint.sh

VOLUME ["/beacon/nginx/certs/beacon.key"]
VOLUME ["/beacon/nginx/certs/beacon.cert"]
VOLUME ["/beacon/config.yml"]
#VOLUME ["/beacon/nginx/service"]

WORKDIR /beacon
USER beacon
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
