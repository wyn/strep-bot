import unittest as ut
from unittest.mock import Mock, patch

from .utils import make_mocks
import create


class TestView(ut.TestCase):

    def test_render(self):
        v = create.View()
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
        'messageId': '4gejUgAGwgq7fMRJD9VV-H___pLGgLkmbQ',
        'payload': {'symphonyElementsAction': {'actionStream': {'streamId': 'tS7YLPuK0HmoyLEw_2zdg3___pLqRcf7dA'},
                                               'formId': 'strep_new',
                                               'formMessageId': 'vmABp90O6YlXc+O8K90VFX///pLGgQ14dA==20297',
                                               'formStream': {'streamId': 'XoMe/OFS08sGhFJLbcGB1X///pLo7HKydA=='},
                                               'formValues': {'action': action,
                                                              'trade_date': '14/09/2019',
                                                              'trade_ticker': 'NASDAQ:VOD'}}},
        'timestamp': 1568627705561,
        'type': 'SYMPHONYELEMENTSACTION'
    }

    def test_shouldUpdateIfCheckButtonAction(self):
        mock_mc, mock_bot, mock_controller = make_mocks()
        cr = create.Response(mock_bot, mock_controller)

        cr.update(self.make_msg(action="reset_button"))
        self.assertEqual(0, mock_controller.render.call_count)
        self.assertEqual(0, mock_mc.send_msg.call_count)

        cr.update(self.make_msg(action="check_button"))
        self.assertEqual(1, mock_controller.render.call_count)
        self.assertEqual(1, mock_mc.send_msg.call_count)


class TestController(ut.TestCase):

    def test_responds_to(self):
        _, mock_bot, mock_controller = make_mocks()
        resp = create.Response(mock_bot, mock_controller)
        view = create.View()
        c = create.Controller(resp, view)
        self.assertEqual("/strep new", c.responds_to)

    def test_render(self):
        _, mock_bot, mock_controller = make_mocks()
        resp = create.Response(mock_bot, mock_controller)
        view = create.View()
        c = create.Controller(resp, view)
        msg = c.render(None).strip()
        self.assertIsNotNone(msg)
        self.assertTrue(msg.startswith("<messageML>"))


if __name__ == '__main__':
    ut.main()
