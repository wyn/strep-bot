from unittest.mock import Mock


def make_mocks():
    mock_mc = Mock()
    mock_bot = Mock()
    mock_bot.get_message_client = Mock(return_value=mock_mc)
    mock_controller = Mock()
    return mock_mc, mock_bot, mock_controller

