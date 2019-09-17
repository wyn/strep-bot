import unittest as ut
from unittest.mock import Mock, patch

import mvc


class ATestController(mvc.GeneralController):

    @property
    def responds_to(self):
        return "boo"

class TestGeneralController(ut.TestCase):

    def test_updateShouldUpdateResponse(self):
        response = Mock()
        view = Mock()
        gc = ATestController(response, view)
        data = Mock()
        gc.update(data)
        response.update.assert_called_once_with(data)

    def test_renderShouldCallViewRender(self):
        response = Mock()
        view = Mock()
        gc = ATestController(response, view)
        data = Mock()
        gc.render(data)
        view.render.assert_called_once_with(data)

    def test_makeFormId(self):
        actual = mvc.GeneralController.make_form_id("/Test me     ")
        self.assertEqual("test_me", actual)


class TestControllers(ut.TestCase):

    def test_addShouldAdd(self):
        c = Mock()
        c.make_form_id = Mock(return_value="key")
        d = dict()
        cs = mvc.Controllers(d)
        cs.add(c)
        c.make_form_id.assert_called_once()
        self.assertTrue("key" in d)
        self.assertEqual(c, d["key"])

    def make_action_msg(self, form_id):
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
                                               'formId': form_id,
                                               'formMessageId': 'vmABp90O6YlXc+O8K90VFX///pLGgQ14dA==20297',
                                               'formStream': {'streamId': 'XoMe/OFS08sGhFJLbcGB1X///pLo7HKydA=='},
                                               'formValues': {'action': 'check_button',
                                                              'trade_date': '14/09/2019',
                                                              'trade_ticker': 'NASDAQ:VOD'}}},
        'timestamp': 1568627705561,
        'type': 'SYMPHONYELEMENTSACTION'
    }

    def make_msg(self):
        return {
            "messageId": "JbfAMr-o5XnaDCYymdXi2n___pLGgaF5bQ",
            "timestamp": 1568627646086,
            "message": "<div data-format=\"PresentationML\" data-version=\"2.0\" class=\"wysiwyg\"><p>/strep new</p></div>",
            "data": "{}",
            "user": {'displayName': 'Ludwig',
                     'email': 'ludwig_van1770@hotmail.com',
                     'firstName': 'Ludwig',
                     'lastName': 'Beethoven',
                     'userId': 1234512345,
                     'username': 'ludwig_van1770@hotmail.com'},
            "stream": {
                "streamId": "XoMe_OFS08sGhFJLbcGB1X___pLo7HKydA",
                "streamType": "ROOM"
            },
            "externalRecipients": False,
            "userAgent": "DESKTOP",
            "originalFormat": "com.symphony.messageml.v2"
        }


    def test_updateShouldUpdateCorrectOne(self):
        c = Mock()
        c.make_form_id = Mock(return_value="key")

        cs = mvc.Controllers()
        cs.add(c)

        msg = self.make_action_msg("key")
        cs.update(msg)
        c.update.assert_called_once_with(msg)

    def test_updateShouldThrowWithWrongFormId(self):
        c = Mock()
        c.make_form_id = Mock(return_value="key")

        cs = mvc.Controllers()
        cs.add(c)

        msg = self.make_action_msg("not_there")
        self.assertRaises(mvc.UnknownCommandError, cs.update, msg)
        c.update.assert_not_called()

    def test_renderShouldRenderCorrectOne(self):
        c = Mock()
        c.make_form_id = Mock(return_value="strep_new")

        cs = mvc.Controllers()
        cs.add(c)

        msg = self.make_msg()
        view = cs.render(msg)
        c.render.assert_called_once_with(msg)
        self.assertTrue(view.startswith("<messageML>"))

    def test_renderShouldThrowWithWrongFormId(self):
        c = Mock()
        c.make_form_id = Mock(return_value="not_there")

        cs = mvc.Controllers()
        cs.add(c)

        msg = self.make_msg()
        self.assertRaises(mvc.UnknownCommandError, cs.render, msg)
        c.render.assert_not_called()


if __name__ == '__main__':
    ut.main()

