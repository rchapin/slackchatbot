# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.8.5-slim

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY ./slackchatbot ./

# Install dependencies.
RUN pip install -r requirements.txt && pip install .

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
ENTRYPOINT ["slackchatbot", "--configfile", "/etc/slackreplybot.yaml"]