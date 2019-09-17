import logging
from sym_api_client_python.clients.datafeed_client import DataFeedClient
import pprint


class DataFeedClient2(DataFeedClient):

    # raw api call to read_datafeed --> returns an array of events returned
    # from DataFeed
    def read_datafeed(self, datafeed_id):
        new_events = super().read_datafeed(datafeed_id)
        for ev in new_events:
            logging.debug(f"new event {pprint.pformat(ev)}")
        return new_events
