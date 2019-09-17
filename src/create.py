import datetime

import jinja2
from jinja2 import Template

from mvc import GeneralController, IResponse, IView
from sym_api_client_python.processors.sym_elements_parser import SymElementsParser
from sym_api_client_python.processors.sym_message_parser import SymMessageParser


class View(IView):

    def render(self, message):

        return """
<messageML>
<form id="{{CreateForm.form_id}}">
    <span>
        <h1>Suspicious Transaction Checker</h1>
        <br/>
        <hr/>
        <br/>
        <h2>Date</h2>
        <text-field
        name="trade_date"
        placeholder="{{CreateForm.trade_date}}"
        required="true"/>

        <h2>Ticker</h2>
        <text-field
        name="trade_ticker"
        placeholder="{{CreateForm.trade_ticker}}"
        required="true"/>
    </span>
    <span>
        <button type="reset">Reset</button>
        <button name="check_button" type="action">Check</button>
    </span>

</form>
</messageML>
"""


class Response(IResponse):

    def __init__(self, bot_client, next_controller, sym_elements_parser=None):
        self._bot_client = bot_client
        self._next_controller = next_controller
        self._elements_parser = sym_elements_parser or SymElementsParser()

    def update(self, action):
        button = self._elements_parser.get_action(action)
        if button == "check_button":
            vals = self._elements_parser.get_form_values(action)
            msg = dict(message=self._next_controller.render(vals))
            streamId = self._elements_parser.get_stream_id(action)
            mc = self._bot_client.get_message_client()
            mc.send_msg(streamId, msg)



class Controller(GeneralController):

    @property
    def responds_to(self):
        return "/strep new"

    def render(self, message):
        form_j = super().render(message)
        t = Template(form_j, trim_blocks=True, lstrip_blocks=True)

        data = {"CreateForm": {"form_id": self.make_form_id(self.responds_to),
                               "trade_date": datetime.date.today().strftime("%d/%m/%y"),
                               "trade_ticker": "NASDAQ:AAPL"}}
        return t.render(data)
