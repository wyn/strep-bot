from exceptions import UnknownCommandError
from sym_api_client_python.listeners.room_listener import RoomListener
from sym_api_client_python.processors.sym_message_parser import SymMessageParser
import calendar
import time
import logging



class GeneralRoomListener(RoomListener):

    def __init__(self, SymBotClient, controllers):
        self._bot_client = SymBotClient
        self._controllers = controllers
        self.msg_processor = SymMessageParser()

    def on_room_msg(self, message):
        logging.debug('room message recieved', message)
        streamId = self.msg_processor.get_stream_id(message)
        logging.debug(f"Stream ID: {streamId}")

        #sample code for developer to implement --> use MessageClient and
        #data recieved from message event to reply with a #reed
        try:
            msg = dict(message=self._controllers.render(message))
        except UnknownCommandError as e:
            logging.debug(e)
        else:
            mc = self._bot_client.get_message_client()
            mc.send_msg(streamId, msg)

    def on_room_created(self, roomCreated):
        logging.debug('room created', roomCreated)

    def on_room_deactivated(self, roomDeactivated):
        logging.debug('room Deactivated', roomDeactivated)

    def on_room_member_demoted_from_owner(self, roomMemberDemotedFromOwner):
        logging.debug('room member demoted from owner', roomMemberDemotedFromOwner)

    def on_room_member_promoted_to_owner(self, roomMemberPromotedToOwner):
        logging.debug('room member promoted to owner', roomMemberPromotedToOwner)

    def on_room_reactivated(self, roomReactivated):
        logging.debug('room reactivated', roomReactivated)

    def on_room_updated(self, roomUpdated):
        logging.debug('room updated', roomUpdated)

    def on_user_joined_room(self, userJoinedRoom):
        logging.debug('USER JOINED ROOM', userJoinedRoom)

    def on_user_left_room(self, userLeftRoom):
        logging.debug('USER LEFT ROOM', userLeftRoom)
