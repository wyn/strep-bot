
import jinja2
from jinja2 import Template

from mvc import GeneralController, IResponse, IView
from sym_api_client_python.processors.sym_elements_parser import SymElementsParser
from sym_api_client_python.processors.sym_message_parser import SymMessageParser


class View(IView):

    def render(self, message):

        return """
<messageML>
    <form id="{{HelpForm.form_id}}">
        <br/>
        <h2>Strep Bot</h2>
        <hr/>
        <br/>
        <p>A bot that lets you check whether a Suspicious Transaction Report is a false positive.</p>
        <p>The Strep Bot queries news feeds for you to see whether there is any publicly available information relating to the trade.</p>
        <p>Currently the only data feed used is Twitter.</p>
        <br/>
        <h5>Commands</h5>

        <ul>

        <li>/strep
          <ul><li>this help menu</li></ul>
        </li>
        <li>/strep new
          <ul><li>check a new suspicious transaction</li></ul>
        </li>

        </ul>
    </form>
</messageML>
"""



class Controller(GeneralController):

    @property
    def responds_to(self):
        return "/strep"

    def render(self, message):
        form_j = super().render(message)
        t = Template(form_j, trim_blocks=True, lstrip_blocks=True)

        data = {"HelpForm": {"form_id": self.make_form_id(self.responds_to)}}

        return t.render(data)

