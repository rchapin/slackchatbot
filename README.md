# Slack Chat Bot


## Configuring in Slack

1. Creating an App

    1.  Once logged into a web browser you HAVE to access the apps page by a separate URL.  This is not at all obvious https://api.slack.com/apps?new_classic_app=1

    1. Enter an App Name and Select the Workspace to which it will belong and click ```Create```.

    2. Under ```Add features and functionality``` click ```Bots```

    3. Then, under ```First, add a legacy bot user``` click on the aforementioned named button.  DO NOT CLICK the "Update Scopes" button

    4. In the left-hand nav, click on ```OAuth & Permissions``` and then click on ```Install App to Workspace``` and then the ```Allow``` button on the next screen.


1. Adding to a channel.  This was the least obvious of all.  As an admin logged in to the workspace vi a web browser there is a "Add an app" blue link underneath the title of the channel.  This does not seem to show up in the thick client, but I am not certain.

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
export OATH_TOKEN=xob-etc

curl -X POST \
-H "Authorization: Bearer $OAUTH_TOKEN" \
-H "Content-type: application/json;charset=utf-8" \
-d @test.json \
https://slack.com/api/chat.postMessage
```
