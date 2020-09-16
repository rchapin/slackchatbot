FROM python:3.8.5

ARG SLACKCHATBOT_VERSION
ARG PYPI_INDEX_URL
ARG PYPI_HOST
ENV APP_DIR /app
ENV PIP_ARGS "--trusted-host $PYPI_HOST --index-url $PYPI_INDEX_URL"

WORKDIR $APP_DIR
RUN \
    python -m venv venv && \
    venv/bin/pip install $PIP_ARGS -U setuptools pip
RUN venv/bin/pip install $PIP_ARGS slackchatbot==$SLACKCHATBOT_VERSION

FROM python:3.8.5-slim

ENV APP_DIR /app
RUN mkdir /etc/slackchatbot
VOLUME ["/etc/slackchatbot"]

WORKDIR $APP_DIR
COPY --from=0 /app .

RUN \
    groupadd -g 10001 slackchatbot && \
    adduser --system --uid 10001 --gid 10001 --home $APP_DIR --no-create-home --shell /bin/nologin slackchatbot

CMD su - slackchatbot -c "source /app/venv/bin/activate && slackchatbot --configfile /etc/slackchatbot/slackchatbot.yaml"
