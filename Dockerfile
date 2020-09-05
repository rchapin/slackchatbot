# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.8

# RUN apt update && apt-get install -y python3-pip

RUN pip install --trusted-host nexus.dmz-svcs.mootley.local slackchatbot==1.0.0.0 --index-url https://nexus.dmz-svcs.mootley.local:8443/repository/pypi-dev/simple -U setuptools pip
RUN pip install --trusted-host nexus.dmz-svcs.mootley.local slackchatbot==1.0.0.0 --index-url https://nexus.dmz-svcs.mootley.local:8443/repository/pypi-dev/simple

ENTRYPOINT ["slackchatbot", "--configfile", "/etc/slackchatbot.yaml"]
# ENTRYPOINT /bin/bash
