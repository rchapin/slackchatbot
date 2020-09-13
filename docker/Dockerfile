FROM python:3.8.5

ARG pypi_repo
ARG version

WORKDIR /app
RUN python -m venv venv \
    && venv/bin/pip install --trusted-host nexus.dmz-svcs.mootley.local \
       --index-url https://nexus.dmz-svcs.mootley.local:8443/repository/${pypi_repo}/simple \
       -U setuptools pip
ENV VERSION $version
RUN venv/bin/pip install --trusted-host nexus.dmz-svcs.mootley.local \
       --index-url https://nexus.dmz-svcs.mootley.local:8443/repository/${pypi_repo}/simple \
       slackchatbot==$VERSION

FROM python:3.8.5-slim

RUN mkdir /etc/slackchatbot
VOLUME ["/etc/slackchatbot"]
RUN groupadd -g 10001 slackchatbot \
   && adduser --uid 10001 --gid 10001 slackchatbot
WORKDIR /app
COPY --from=0 /app .

CMD su - slackchatbot -c "source /app/venv/bin/activate && slackchatbot --configfile /etc/slackchatbot/slackchatbot.yaml"
