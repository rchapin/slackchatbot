import yaml
from slack import RTMClient

class SlackChatBot(object):

    def __init__(self, args, logger):
        self.args = args
        self.logger = logger
        self.configs = SlackChatBot.load_configs(args.configfile)
        self.rtm_client = SlackChatBot.get_rtm_slack_client(
            self.configs['bot_user_oauth_token'])

    def run(self):
        RTMClient.on(event="message", callback=self.process_message)
        self.rtm_client.start()
#
#     def say_hello(self, **payload):
#         data = payload["data"]
#         if data:
#             if "text" in data:
#                 text = data["text"]
#                 self.textChanged.emit(text)

    @staticmethod
    def load_configs(config_file_path):
        with open(config_file_path, 'r') as fh:
            return yaml.load(fh, Loader=yaml.FullLoader)

    @staticmethod
    def get_rtm_slack_client(bot_token):
        return RTMClient(token=bot_token)

    def get_message_to_parse(self, payload):
        '''
        Parses the payload from Slack and return the message to which we
        will be responding.
        '''
        web_client = payload['web_client']
        data = payload.get('data', None)
        ts = float(data.get('ts', 0))
        channel = data.get('channel', None)
        if data is not None:
            message = data.get('message', None)
            if message:
                '''
                If there is a message key this is a parent message. We need to query
                for the threaded replies
                '''
                thread_ts = message.get('thread_ts')
                response = web_client.conversations_replies(
                    channel=channel,
                    ts=thread_ts,
                    token=self.configs['oauth_access_token'])
                # FIXME: Add try/except
                response = response.validate()
                messages = response.get('messages')
                if messages:
                    '''
                    We are going to assume that if we were up and running up
                    until now that we will have already read all but the most
                    recent messages, so we will just attempt to parse the
                    message
                    '''
                    if len(messages) > 0:
                        message = messages[-1]
                        print('foo')
            else:
                # This is an unthreaded message as of yet
                print('foo')

    def get_message_from_thread(self):
        pass

    def process_message(self, **payload):
        data = payload['data']
        ts = float(data.get('ts', 0))
        channel = data.get('channel', None)
        web_client = payload['web_client']
        bot_id = data.get('bot_id', '')

        # Get the message to which we will be responsing
        message = self.get_message_to_parse(payload)

        # If a message is not send by the bot
        if bot_id == "":
            channel_id = data["channel"]
            # Extracting message send by the user on the slack
            text = data.get("text", "")
            text = text.split(">")[-1].strip()

            response = ""
            if "help" in text.lower():
                user = data.get("user", "")
                response = f"Hi <@{user}>! :)"

                web_client.chat_postMessage(
                    channel=channel_id,
                    text=response)

#         if 'Hello' in data['text']:
#             channel_id = data['channel']
#             thread_ts = data['ts']
#             # This is not username but user ID (the format is ei``ther U*** or W***)
#             user = data['user']
#
#             web_client.chat_postMessage(
#                 channel=channel_id,
#                 text=f"Hi <@{user}>!",
#                 thread_ts=thread_ts
#             )
