from datetime import datetime
import asyncio
import signal
import yaml
from slack import RTMClient
from slack.web.client import WebClient

class SlackChatBot(object):

    def __init__(self, args, logger):
        self.args = args
        self.logger = logger
        self.configs = SlackChatBot.load_configs(args.configfile)
        # TODO: add a timeout to the WebClient timeout=30?
        self.web_client = WebClient(token=self.configs['bot_user_oauth_token'])
        self.bot_id = self.web_client.api_call("auth.test")['user_id']

    @staticmethod
    def load_configs(config_file_path):
        with open(config_file_path, 'r') as fh:
            return yaml.load(fh, Loader=yaml.FullLoader)

    def get_message_to_parse(self, data):
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
            web_client = WebClient(token=self.configs['oauth_access_token'])
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

    def generate_message_response(self, message):
        retval = None
        if 'Hello' in message['text']:
            retval = f'Hello to you to :)'
        return retval

    def get_message_from_thread(self):
        pass

    async def process_message(self, **payload):
        data = payload['data']
        user = data.get('user', None)
        if user == None or user == self.bot_id:
            self.logger.debug('Ignoring messages from myself')
            return

        self.logger.debug(f'data={data}')
        channel = data.get('channel', None)

        '''
        Get the message to which we will be responding and then determine
        our response
        '''
        message = self.get_message_to_parse(data)

        thread_ts = data.get('ts')
        parent_ts = message.get('parent_ts', None)
        message_thread_ts = message.get('thread_ts', None)
        target_ts = self.get_target_timestamp(parent_ts, message_thread_ts, thread_ts)

        message_response = self.generate_message_response(message)
        if message_response is not None:
#             target_ts = parent_ts if parent_ts is not None else thread_ts
            self.logger.debug(f"responding to user= with={message_response}")
            web_client = WebClient(self.configs['bot_user_oauth_token'])
            response = web_client.chat_postMessage(
                channel=channel,
                text=message_response,
                thread_ts=target_ts)
            self.logger.debug(f'response from posting reply={response}')

            '''
            For the time-being we will assume that for any response we will star
            and check the parent thread.
            '''
            response = web_client.reactions_add(
                channel=channel,
                timestamp=target_ts,
                name='star')
            response = web_client.reactions_add(
                channel=channel,
                timestamp=target_ts,
                name='heavy_check_mark')
        else:
            self.logger.debug(f"user= sent a message we ignored")

        self.logger.info(f'Message processed for user={user}, target_ts={target_ts}')

    def get_target_timestamp(self, parent_ts, message_thread_ts, thread_ts):
        if parent_ts is not None:
            return parent_ts
        if message_thread_ts is not None:
            return message_thread_ts
        return thread_ts

    async def run_loop(self):
        while self.running:
            print(f'Checking running={self.running}, {datetime.now()}')
            await asyncio.sleep(3)
            if not self.running:
                print('Stopping RTMClient....')
                self.rtm_client.stop()

    async def api_test_loop(self):
        while self.running:
            print(f'api test {datetime.now()}')
            response = self.web_client.api_call('api.test')
            # Do something if this fails
            print(response)
            await asyncio.sleep(10)

    async def run(self):
        self.loop = asyncio.get_event_loop()
        self.web_client = WebClient(token=self.configs['bot_user_oauth_token'])
        self.rtm_client = RTMClient(token=self.configs['bot_user_oauth_token'], run_async=True, loop=self.loop)
        self.rtm_client.on(event='message', callback=self.process_message)
        self.running = True

        await asyncio.gather(
            self.register_signal_handlers(),
            self.rtm_client.start(),
            self.run_loop(),
            self.api_test_loop()
        )
        print('Run complete...')

    async def register_signal_handlers(self):
        print('Registering signal hanlders')
        signals = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT)
        for s in signals:
            signal.signal(s, self.shutdown)
        return

    def shutdown(self, *unused):
        print(f'Shutdown called')
        self.running = False