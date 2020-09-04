import sys
import logging
import argparse
from slackchatbot.lib.slackchatbot import SlackChatBot

'''
Only logging to the console as we assume that this will run either in a
container and/or under systemd and that all logs will be collected by
something that can manage STDOUT and STDERR appropriately.
'''
LOGGING_FORMAT = '%(asctime)s,%(levelname)s,%(module)s,%(message)s'
logging.basicConfig(
    format=LOGGING_FORMAT,
    level=logging.INFO,
    stream=sys.stdout)
logger = logging.getLogger(__name__)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--configfile',
        type=str,
        required=True,
        help='Fully qualified path to the config yaml file')

    parser.add_argument(
        '--loglevel',
        type=str,
        default='INFO',
        help='logging output level configuration')

    return parser.parse_args()

def main():
    args = parse_args()

#     formatter = logging.Formatter(LOGGING_FORMAT)
#     console_handler = logging.StreamHandler(sys.stdout)
#     console_handler.setFormatter(formatter)
#     logger.addHandler(console_handler)
#     logger.setLevel(args.loglevel.upper())

    logger.info(f'slackreplybot run with args={args}')
    logger.debug('debugging')

    slackchatbot = SlackChatBot(args, logger)
    slackchatbot.run()


###############################################################################
# MAIN
###############################################################################

if __name__ == '__main__':
    main()