FROM python:3.8.5

ARG PYPI_INDEX_URL
ARG PYPI_HOST
ARG SLACKCHATBOT_VERSION
ENV APP_DIR /app
ENV PIP_ARGS "--trusted-host $PYPI_HOST --index-url $PYPI_INDEX_URL"

WORKDIR $APP_DIR
RUN \
    python -m venv venv && \
    venv/bin/pip install $PIP_ARGS -U setuptools pip
RUN venv/bin/pip install $PIP_ARGS slackchatbot==$SLACKCHATBOT_VERSION

FROM python:3.8.5-slim

RUN mkdir /etc/slackchatbot
VOLUME ["/etc/slackchatbot"]
RUN \
    groupadd -g 10001 slackchatbot && \
    adduser --system --uid 10001 --gid 10001 slackchatbot --home $APP_DIR --shell /bin/nologin

WORKDIR $APP_DIR
COPY --from=0 /app .

CMD su - slackchatbot -c "source /app/venv/bin/activate && slackchatbot --configfile /etc/slackchatbot/slackchatbot.yaml"
