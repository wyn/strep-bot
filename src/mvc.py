from abc import ABC, abstractmethod
import os.path
import logging
from exceptions import UnknownCommandError, FailedCommandError
from sym_api_client_python.processors.sym_elements_parser import SymElementsParser
from sym_api_client_python.processors.sym_message_parser import SymMessageParser


# responses and views

class IResponse(ABC):

    @abstractmethod
    def update(self, action):
        pass


class NullResponse(IResponse):

    def update(self, action):
        pass


class IView(ABC):

    @abstractmethod
    def render(self, message):
        pass


# Controller interfaces and classes

class IResponds(ABC):

    @property
    @abstractmethod
    def responds_to(self):
        pass

class IController(ABC):

    @abstractmethod
    def update(self, action):
        pass

    @abstractmethod
    def render(self, message):
        pass

class GeneralController(IController, IResponds):

    def __init__(self, response, view):
        self._response = response
        self._view = view

    def update(self, action):
        self._response.update(action)

    def render(self, message):
        return self._view.render(message)

    @staticmethod
    def make_form_id(cmd):
        return cmd.strip().lower().replace('/', '').replace(' ', '_')


class Controllers(IController):

    def __init__(self, controllers=None):
        self._controllers = controllers if controllers is not None else {}
        self._msg_parser = SymMessageParser()
        self._elements_parser = SymElementsParser()

    def update(self, action):
        ky = self._elements_parser.get_form_id(action)
        try:
            c = self._controllers[ky]
        except KeyError:
            raise UnknownCommandError(ky)
        c.update(action)

    def render(self, message):
        msg = ' '.join(self._msg_parser.get_text(message))
        ky = GeneralController.make_form_id(msg)
        try:
            c = self._controllers[ky]
        except KeyError:
            raise UnknownCommandError(msg)
        return c.render(message)

    def add(self, controller):
        ky = controller.make_form_id(controller.responds_to)
        self._controllers[ky] = controller

