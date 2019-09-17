from exceptions import FailedCommandError, UnknownCommandError
from sym_api_client_python.listeners.elements_listener import ElementsActionListener
from sym_api_client_python.processors.sym_elements_parser import SymElementsParser
import logging


class GeneralElementsListener(ElementsActionListener):
    """Example implementation of ElementsActionListener

        sym_bot_client: contains clients which respond to incoming events

    """

    def __init__(self, sym_bot_client, controllers):
        self._bot_client = sym_bot_client
        self._controllers = controllers
        self._parser = SymElementsParser()

    def on_elements_action(self, action):
        logging.debug('element submitted :')
        try:
            self._controllers.update(action)
        except UnknownCommandError as e:
            logging.debug(e)
        except FailedCommandError as e:
            logging.error(e)
            streamId = self._parser.get_stream_id(action)
            mc = self._bot_client.get_message_client()
            err = str(e)
            mc.send_msg(streamId, dict(message=f"<messageML>{err}</messageML>"))
