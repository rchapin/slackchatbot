# Slack Chat Bot


## Configuring in Slack

1. Creating an App

    1.  Once logged into a web browser you HAVE to access the apps page by a separate URL.  This is not at all obvious https://api.slack.com/apps?new_classic_app=1

    1. Enter an App Name and Select the Workspace to which it will belong and click ```Create```.

    1. Under ```Add features and functionality``` click ```Bots```

    1. Then, under ```First, add a legacy bot user``` click on the ```Add Legacy Bot User``` button.  DO NOT CLICK the ```Update Scopes``` button!

    1. Enter a name and username for the bot.

    1. Click on ```Oauth & Permissions``` in the left-hand nav and the following additional OAuth Scopes.  Scroll down about 1/2 on the page until you see the ```Scopes``` section.  DO NOT click on ```Update Scopes```, click on the ```Add an OAuth Scope``` and add the following scopes:

        - channels:history
        - groups:history
        - mpim:history
        - im:history
        - chat:write:bot

    1. In the left-hand nav, click on ```OAuth & Permissions``` and then click on ```Install App to Workspace``` and then the ```Allow``` button on the next screen.

    1. On the resulting screen, copy and paste the OAuth tokens into the yaml config file.

1. Adding the bot to a channel. In the channel to which you want to invite the bot, type the following command ```/invite @<username>``` in the message field. 

1. Test the credentials.

    1. Create the following ```test.json``` file

    ```
    {
      "channel":"#my-channel",
      "text":"Hello, World!"
    }
    ```

    2. Export the following env var and run the following command

```
export OAUTH_TOKEN=<xob-etc>

curl -X POST \
-H "Authorization: Bearer $OAUTH_TOKEN" \
-H "Content-type: application/json;charset=utf-8" \
-d @test.json \
https://slack.com/api/chat.postMessage
```

## Deployment

1. Ensure that you have the docker service installed on the host.

1. Test docker and configure the firewall.

    ```
    docker run hello-world
    ```

1.  Add a ```slackchatbot``` user to the host so that we can run the docker container as a non-root user.

    1. Added slackbot group and on the docker host.  We specify the GID and UID because that is what the UID is in the docker image that we will be using.

    ```
    groupadd -g 10001 -r slackchatbot && useradd -r -g slackchatbot -u 10001 slackchatbot && usermod -a -G docker slackchatbot
    ```

1.  Create named volumes for the slackchatbot container and set the permissions

    1. Named volume for config files

    ```
    docker volume create --name slackchatbot-etc
    chmod 755 /var/lib/docker
    chmod 755 /var/lib/docker/volumes
    ```

1.  Copy the config file to the directory for the slackchatbot-etc dir and chown for slackchatbot

1.  Create the log dir and set the permissions.

    ```
    mkdir -p /var/log/slackchatbot
    chown -R slackchatbot: /var/log/slackchatbot
    ```

1. Install the syslog configs and systemd unit file

    1. Copy the etc/systemd/system/slackchatbot.service file to /etc/systemd/system

    ```
    restorecon -v /etc/systemd/system/slackchatbot.service
    systemctl daemon-reload
    ```

    1. Copy the rsyslog.d config file from ```etc/rsyslog.d/slackchatbot.conf``` to ```/etc/rsyslog.d``` so that all of the logs from the container will go to a dedicated log file.

    ```
    restorecon -v /etc/rsyslog.d/slackchatbot.conf
    systemctl restart rsyslog
    ```

1. Start up and configure slackchatbot:

    ```
    systemctl start slackchatbot
    ```
