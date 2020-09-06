import asyncio
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
STATS_FORMAT = '%(module)s %(message)s'

logger = logging.getLogger(__name__)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--configfile',
        type=str,
        required=True,
        help='Fully qualified path to the config yaml file')

    parser.add_argument(
        '--dryrun',
        type=str,
        required=True,
        help='Will just log questions and answers and not respond')

    parser.add_argument(
        '--loglevel',
        type=str,
        default='INFO',
        help='logging output level configuration')

    return parser.parse_args()

def main():
    args = parse_args()

    # Reconfigure the basic logging to pick up our defined log level
    logging.getLogger().setLevel(args.loglevel.upper())
    logger.info(f'slackreplybot run with args={args}')

    '''
    Create a stats logger to which we will only publish stats. We will
    ultimately move this to use OpenTelemetry.
    '''
    stats_logger = logging.getLogger('slackchatbot_stats')
    loggers = dict(
        logger=logger,
        stats_logger=stats_logger,
        )

    slackchatbot = SlackChatBot(loggers, args)
    asyncio.run(slackchatbot.run())
    logger.info('SlackReplyBot complete')

###############################################################################
# MAIN
###############################################################################

if __name__ == '__main__':
    main()