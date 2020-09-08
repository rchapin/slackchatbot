import logging
import unittest
from unittest.mock import MagicMock
from slackchatbot.lib.slackchatbot import SlackChatBot

HTR_TEST_RESPONSES_AB = 'This is the AB response'
HTR_TEST_RESPONSES_CD = 'This is another response, but for CD this time'
HTR_TEST_RESPONSES_XY = 'This is the YX response'
HTR_TEST_RESPONSES_ABC123 = 'This is the ABC123 response'

HTR_TEST_RESPONSES = {
    'ab': HTR_TEST_RESPONSES_AB,
    'cd': HTR_TEST_RESPONSES_CD,
    'xy': HTR_TEST_RESPONSES_XY,
    'abc123': HTR_TEST_RESPONSES_ABC123
    }

class SlackChatBotTests(unittest.TestCase):

    def test_process_htr_message(self) -> None:
        mock_args = MagicMock()
        mock_logger = MagicMock()
        mock_logger.info = MagicMock(side_effect=None)
        mock_stats_logger = MagicMock()
        mock_stats_logger.info = MagicMock(side_effect=None)
        mock_loggers = dict(
            logger=mock_logger,
            stats_logger=mock_stats_logger,
            )

        slackchatbot = SlackChatBot(mock_loggers, mock_args)
        slackchatbot._set_htr_responses(HTR_TEST_RESPONSES)

        test_data = [
            {
                'test_message': {'text': 'ab?'},
                'expected_msg_bool': True,
                'expected_answer': HTR_TEST_RESPONSES_AB,
                },
            {
                'test_message': {'text': 'cd?'},
                'expected_msg_bool': True,
                'expected_answer': HTR_TEST_RESPONSES_CD,
                },
            {
                'test_message': {'text': 'xy?'},
                'expected_msg_bool': True,
                'expected_answer': HTR_TEST_RESPONSES_XY,
                },
            {

                'test_message': {'text': 'rc?'},
                'expected_msg_bool': False,
                'expected_answer': None,
                },
            {

                'test_message': {'text': 'abc123?'},
                'expected_msg_bool': True,
                'expected_answer': HTR_TEST_RESPONSES_ABC123,
                },
            ]

        for t in test_data:
            actual_msg_bool, actual_answer = slackchatbot.process_htr_message(t['test_message'])
            self.assertEqual(t['expected_msg_bool'], actual_msg_bool, f'for test_data={t}')
            self.assertEqual(t['expected_answer'], actual_answer, f'for test_data={t}')

