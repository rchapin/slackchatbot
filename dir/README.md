# Slack Chat Bot


## Configuring in Slack

1. Creating an App

    1.  Once logged into a web browser you HAVE to access the apps page by a separate URL.  This is not at all obvious https://api.slack.com/apps?new_classic_app=1

    1. Enter an App Name and Select the Workspace to which it will belong and click ```Create```.

    1. Under ```Add features and functionality``` click ```Bots```

    1. Then, under ```First, add a legacy bot user``` click on the ```Add Legacy Bot User``` button.  DO NOT CLICK the ```Update Scopes``` button!

    1. Enter a name and username for the bot.

    1. Add the following additional OAuth Scopes

channels:history,groups:history,mpim:history,im:history,chat:write:bot

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
