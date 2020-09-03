import asyncio
import os
from datetime import datetime
import signal
import slack
from slack.web.client import WebClient

class SlackTest(object):

    def __init__(self):
        self.token = os.environ.get('BOT_TOKEN', None)

    async def process_message(self, **payload):
        data = payload['data']
        print(data.get('text'))

    async def run_loop(self):
        while self.running:
            print(f'Checking running={self.running}, {datetime.now()}')
            await asyncio.sleep(3)
            if not self.running:
                print('Stopping RTMClient....')
                self.rtm_client.stop()

    async def ping_loop(self):
        while self.running:
            print(f'api test {datetime.now()}')
            response = self.web_client.api_call('api.test')
            # Do something if this fails
            print(response)
            await asyncio.sleep(10)

    async def run(self):
        self.loop = asyncio.get_event_loop()
        self.web_client = WebClient(token=self.token)
        self.rtm_client = slack.RTMClient(token=self.token, run_async=True, loop=self.loop)
        self.rtm_client.on(event='message', callback=self.process_message)
        self.running = True

        await asyncio.gather(
            self.register_signal_handlers(),
            self.rtm_client.start(),
            self.run_loop(),
            self.ping_loop()
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

if __name__ == "__main__":
    slackTest = SlackTest()
    asyncio.run(slackTest.run())
    print('SlackTest shutdown')
