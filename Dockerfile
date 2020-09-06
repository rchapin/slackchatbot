# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.8

WORKDIR /app

RUN mkdir /etc/slackchatbot
VOLUME ["/etc/slackchatbot"]

RUN groupadd -g 10001 slackchatbot \
   && adduser --uid 10001 --gid 10001 slackchatbot

RUN python -m venv venv \
    && venv/bin/pip install --trusted-host nexus.dmz-svcs.mootley.local \
       --index-url https://nexus.dmz-svcs.mootley.local:8443/repository/pypi-dev/simple \
       -U setuptools pip

ENV VERSION 1.0.0.2
RUN venv/bin/pip install --trusted-host nexus.dmz-svcs.mootley.local \
       --index-url https://nexus.dmz-svcs.mootley.local:8443/repository/pypi-dev/simple \
       slackchatbot==$VERSION

CMD su - slackchatbot -c "source /app/venv/bin/activate && slackchatbot --configfile /etc/slackchatbot/slackchatbot.yaml"
