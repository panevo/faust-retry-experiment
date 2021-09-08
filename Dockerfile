
FROM python:3.7-slim

RUN echo 'deb [check-valid-until=no] http://archive.debian.org/debian jessie-backports main' >> /etc/apt/sources.list \
    && apt-get update && apt-get install -y netcat make && apt-get autoremove -y


ENV PIP_FORMAT=legacy
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /test_acks/

COPY . /test_acks

RUN make install-production



# Create unprivileged user
RUN groupadd --non-unique --gid 1000 faust && adduser --disabled-password --uid 1000 --gid 1000 faust
RUN chown -R faust:faust /test_acks
USER faust

ENTRYPOINT ["./scripts/run"]
