
import jinja2
from jinja2 import Template

from mvc import GeneralController, IResponse, IView
from sym_api_client_python.processors.sym_elements_parser import SymElementsParser
from sym_api_client_python.processors.sym_message_parser import SymMessageParser


class View(IView):

    def render(self, message):

        return """
<messageML>
    <form id="{{SummaryForm.form_id}}">
        <h1>Suspicious Transaction Checker</h1>
        <br/>
        <hr/>
        <br/>
        <h4>You submitted {{SummaryForm.total}} pieces of evidence</h4>
        <br/>
        {{SummaryForm.summary}}
    </form>
</messageML>
"""



class Controller(GeneralController):

    @property
    def responds_to(self):
        return "/strep summary"

    def _gen_counter(self, message):
        # {'action': 'register_button', 'tablesel-row-3': 'on', 'tablesel-row-4': 'on'}
        for ky, vl in message.items():
            if ky.startswith("tablesel-row") and vl == "on":
                yield 1

    def render(self, message):
        form_j = super().render(message)
        t = Template(form_j, trim_blocks=True, lstrip_blocks=True)

        total = sum(self._gen_counter(message))

        data = {"SummaryForm": {"form_id": self.make_form_id(self.responds_to),
                                "total": total,
                                "summary": "<h2>Confirmed False Positive</h2>" if total > 0 else "<h2>Transaction needs further investigation</h2>" }}
        return t.render(data)
