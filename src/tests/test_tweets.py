import unittest as ut
from unittest.mock import Mock, patch
import os, json

from .utils import make_mocks
import tweets


class TestView(ut.TestCase):

    def test_render(self):
        v = tweets.View()
        msg = v.render(None).strip()
        self.assertIsNotNone(msg)
        self.assertTrue(msg.startswith("<messageML>"))


class TestResponse(ut.TestCase):

    def make_msg(self, action):
        return {
        'id': 'yGIDB9',
        'initiator': {'user': {'displayName': 'Ludwig',
                               'email': 'ludwig_van1770@hotmail.com',
                               'firstName': 'Ludwig',
                               'lastName': 'Beethoven',
                               'userId': 1234512345,
                               'username': 'ludwig_van1770@hotmail.com'}},
        'messageId': '1lSz4V29A7gYWoTHFcNvTn___pLGgS8abQ',
        'payload': {'symphonyElementsAction': {'actionStream': {'streamId': 'tS7YLPuK0HmoyLEw_2zdg3___pLqRcf7dA'},
                                               'formId': 'strep_tweets',
                                               'formMessageId': 'Y8kWhkOpQesfMief9C6ipX///pLGgVK1dA==20250',
                                               'formStream': {'streamId': 'XoMe/OFS08sGhFJLbcGB1X///pLo7HKydA=='},
                                               'formValues': {'action': action,
                                                              'tablesel-row-1': 'on',
                                                              'tablesel-row-3': 'on',
                                                              'tablesel-row-4': 'on'}}},
        'timestamp': 1568627705561,
        'type': 'SYMPHONYELEMENTSACTION'
    }

    def test_shouldUpdateIfCheckButtonAction(self):
        mock_mc, mock_bot, mock_controller = make_mocks()
        cr = tweets.Response(mock_bot, mock_controller)

        cr.update(self.make_msg(action="reset_button"))
        self.assertEqual(0, mock_controller.render.call_count)
        self.assertEqual(0, mock_mc.send_msg.call_count)

        cr.update(self.make_msg(action="register_button"))
        self.assertEqual(1, mock_controller.render.call_count)
        self.assertEqual(1, mock_mc.send_msg.call_count)


def gen_from_json(filename):
    data = {}
    with open(filename) as f:
        data = json.load(f)

    def _inner(ticker='NASDAQ:AAPL'):
        for result in data['statuses']:
            yield result

    return _inner


class TestController(ut.TestCase):

    def test_responds_to(self):
        _, mock_bot, mock_controller = make_mocks()
        resp = tweets.Response(mock_bot, mock_controller)
        view = tweets.View()
        c = tweets.Controller(resp, view)
        self.assertEqual("/strep tweets", c.responds_to)

    def test_render(self):
        _, mock_bot, mock_controller = make_mocks()
        resp = tweets.Response(mock_bot, mock_controller)
        view = tweets.View()
        fname = os.path.join(os.path.dirname(__file__), "aapl_example_tweet.json")
        gen_tweets = gen_from_json(fname)
        c = tweets.Controller(resp, view, gen_tweets)
        message = {
            "action": "check_button",
            "trade_date": "14/09/2019",
            "trade_ticker": "NASDAQ:VOD"
        }

        msg = c.render(message).strip()
        self.assertIsNotNone(msg)
        self.assertTrue(msg.startswith("<messageML>"))


if __name__ == '__main__':
    ut.main()
