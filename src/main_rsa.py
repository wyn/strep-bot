import sys

def is_venv():
    return (hasattr(sys, 'real_prefix') or
            (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix))

if is_venv():
    print('In virtual environment. Proceeding.')
else:
    print('Not running in virtual environment. Consider exiting program with ctrl-c') 
    print('Docs for setting up virtual environment:')
    print('https://docs.python.org/3/library/venv.html')



import logging
from sym_api_client_python.configure.configure import SymConfig
from sym_api_client_python.auth.rsa_auth import SymBotRSAAuth
from sym_api_client_python.clients.sym_bot_client import SymBotClient

from room_listener import GeneralRoomListener
from datafeed_imp import DataFeedClient2
from elements_listener import GeneralElementsListener
import mvc
import create
import tweets
import info
import summary


def configure_logging():
        logging.basicConfig(
                filename='./logs/example.log',
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                filemode='w', level=logging.DEBUG
        )
        logging.getLogger("urllib3").setLevel(logging.WARNING)

def main():
        print('Python Client runs using RSA authentication')

        # Configure log
        configure_logging()

        # RSA Auth flow: pass path to rsa config.json file
        configure = SymConfig('../resources/config.json')
        configure.load_config()
        auth = SymBotRSAAuth(configure)
        auth.authenticate()

        # Initialize SymBotClient with auth and configure objects
        bot_client = SymBotClient(auth, configure)
        df = DataFeedClient2(bot_client)
        bot_client.datafeed_client = df

        # Initialize datafeed service
        datafeed_event_service = bot_client.get_datafeed_event_service()

        # Initialize listener objects and append them to datafeed_event_service
        # Datafeed_event_service polls the datafeed and the event listeners
        # respond to the respective types of events
        null_response = mvc.NullResponse()

        controllers = mvc.Controllers()

        controllers.add(info.Controller(null_response, info.View()))
        cc = summary.Controller(null_response, summary.View())
        c = tweets.Controller(tweets.Response(bot_client, cc), tweets.View())
        controllers.add(c)
        controllers.add(create.Controller(create.Response(bot_client, c), create.View()))

        room_listener_test = GeneralRoomListener(bot_client, controllers)
        datafeed_event_service.add_room_listener(room_listener_test)
        elements_listener_test = GeneralElementsListener(bot_client, controllers)
        datafeed_event_service.add_elements_listener(elements_listener_test)

        # Create and read the datafeed
        print('Starting datafeed')
        datafeed_event_service.start_datafeed()


if __name__ == "__main__":
    main()

