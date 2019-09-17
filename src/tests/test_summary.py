import unittest as ut
from unittest.mock import Mock, patch

from mvc import NullResponse
import summary


class TestView(ut.TestCase):

    def test_render(self):
        v = summary.View()
        msg = v.render(None).strip()
        self.assertIsNotNone(msg)
        self.assertTrue(msg.startswith("<messageML>"))


class TestController(ut.TestCase):

    def test_responds_to(self):
        resp = NullResponse()
        view = summary.View()
        c = summary.Controller(resp, view)
        self.assertEqual("/strep summary", c.responds_to)

    def test_render(self):
        resp = NullResponse()
        view = summary.View()
        c = summary.Controller(resp, view)
        message = {'action': 'register_button',
                   'tablesel-row-1': 'on',
                   'tablesel-row-3': 'on',
                   'tablesel-row-4': 'on'}
        msg = c.render(message).strip()
        self.assertIsNotNone(msg)
        self.assertTrue(msg.startswith("<messageML>"))
        self.assertTrue("3 pieces of evidence" in msg)


if __name__ == '__main__':
    ut.main()
