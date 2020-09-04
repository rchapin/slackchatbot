import yaml
from slack import RTMClient
from slack.web.client import WebClient

class SlackChatBot(object):

    configs = None
    logger = None

    def __init__(self, args, logger):
        self.args = args
        SlackChatBot.logger = logger
        SlackChatBot.configs = SlackChatBot.load_configs(args.configfile)
        self.rtm_client = SlackChatBot.get_rtm_slack_client(
            SlackChatBot.configs['bot_user_oauth_token'])

    def run(self):
        self.rtm_client.on(event='message', callback=SlackChatBot.process_message)
        self.rtm_client.start()

    @staticmethod
    def load_configs(config_file_path):
        with open(config_file_path, 'r') as fh:
            return yaml.load(fh, Loader=yaml.FullLoader)

    @staticmethod
    def get_rtm_slack_client(bot_token):
        return RTMClient(token=bot_token)

    @staticmethod
    def get_message_to_parse(data):
        '''
        Parses the payload from Slack and return the message to which we
        will be responding.
        '''
        channel = data.get('channel', None)
        retval = None
        message = data.get('message', None)
        if message:
            '''
            If there is a message key this is a parent message. We need to query
            for the threaded replies
            '''
            parent_ts = message.get('ts')
            web_client = WebClient(token=SlackChatBot.configs['oauth_access_token'])
            response = web_client.conversations_replies(
                channel=channel,
                ts=parent_ts)
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
                    retval = messages[-1]
                    # Document
                    retval['parent_ts'] = parent_ts
        else:
            # This is an unthreaded/parent message
            retval = data

        return retval

    @staticmethod
    def generate_message_response(payload, message):
        retval = ''
        if 'Hello' in message['text']:
            retval = f'Hello to you to :)'
        else:
            retval = 'This is a canned response'
        return retval

    def get_message_from_thread(self):
        pass

    @staticmethod
    def process_message(**payload):
        data = payload['data']
        SlackChatBot.logger.debug(f'data={data}')
        subtype = data.get('subtype', None)
        if subtype is not None and subtype == 'message_replied':
            SlackChatBot.logger.debug('returning, this is a message_replied')
            return
        channel = data.get('channel', None)
        '''
        Following the https://api.slack.com/methods/chat.postMessage
        '''
        thread_ts = data.get('ts')
        bot_id = data.get('bot_id', '')
        if bot_id != '':
            SlackChatBot.logger.debug('returning, this is a bot response')
            return

        '''
        Get the message to which we will be responding and then determine
        our response
        '''
        message = SlackChatBot.get_message_to_parse(data)
        parent_ts = message.get('parent_ts', None)
#         thread_ts = parent_ts if parent_ts is not None else thread_ts
        message_response = SlackChatBot.generate_message_response(payload, message)

        web_client = WebClient(SlackChatBot.configs['bot_user_oauth_token'])
        response = web_client.chat_postMessage(
            channel=channel,
            text=message_response,
            thread_ts=thread_ts)
#         if parent_ts is None:
#             response = web_client.reactions_add(
#                 channel=channel,
#                 timestamp=thread_ts,
#                 name='star')
#             response = web_client.reactions_add(
#                 channel=channel,
#                 timestamp=thread_ts,
#                 name='heavy_check_mark')
#             as_user=False,
#             username='Chat Bot':heavy_check_mark:)

        SlackChatBot.logger.info(f'process_message end {thread_ts}, parent_ts={parent_ts}')

        # Extracting message send by the user on the slack
#         text = data.get("text", "")
#         text = text.split(">")[-1].strip()
#
#         response = ""
#         if "help" in text.lower():
#             user = data.get('user', "")
#             response = f"Hi <@{user}>! :)"
#
#             web_client.chat_postMessage(
#                 channel=response['channel'],
#                 text=response['text'],
#                 thread_ts=reso)
