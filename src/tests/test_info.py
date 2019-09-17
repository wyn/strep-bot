import unittest as ut
from unittest.mock import Mock, patch

from mvc import NullResponse
import info


class TestView(ut.TestCase):

    def test_render(self):
        v = info.View()
        msg = v.render(None).strip()
        self.assertIsNotNone(msg)
        self.assertTrue(msg.startswith("<messageML>"))


class TestController(ut.TestCase):

    def test_responds_to(self):
        resp = NullResponse()
        view = info.View()
        c = info.Controller(resp, view)
        self.assertEqual("/strep", c.responds_to)

    def test_render(self):
        resp = NullResponse()
        view = info.View()
        c = info.Controller(resp, view)
        msg = c.render(None).strip()
        self.assertIsNotNone(msg)
        self.assertTrue(msg.startswith("<messageML>"))


if __name__ == '__main__':
    ut.main()
