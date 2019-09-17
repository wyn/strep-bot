import json
import logging
from datetime import datetime
import os

import jinja2
from jinja2 import Template

from twython import Twython

from mvc import GeneralController, IResponse, IView
from sym_api_client_python.processors.sym_elements_parser import SymElementsParser
from sym_api_client_python.processors.sym_message_parser import SymMessageParser

def gen_from_twitter(creds_filename):
    creds = {}
    with open(creds_filename) as f:
        creds = json.load(f)

    def _inner(ticker='NASDAQ:AAPL'):
        # Instantiate an object
        python_tweets = Twython(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])
        results = python_tweets.search(q=ticker,
                                       result_type='recent',
                                       count=10,
                                       lang='en')
        for result in results['statuses']:
            yield result
    return _inner

def gen_table_rows(dt, gen):
    for result in gen:
        created_at = result['created_at']
        created_at_strs = created_at.split(' ')
        date_str = ' '.join([created_at_strs[2], created_at_strs[1], created_at_strs[-1]])
        tweet_dt = datetime.strptime(date_str, '%d %b %Y')
        urls = result['entities']['urls']
        if tweet_dt <= dt:
            if urls:
                yield dict(created_at=created_at,
                           text=result['text'],
                           url=urls[0]['expanded_url'])
            else:
                yield dict(created_at=result['created_at'],
                           text=result['text'],
                           url="")


class View(IView):

    def render(self, message):
        return """
<messageML>
    <form id="{{TweetsForm.form_id}}">
        <h1>Suspicious Transaction Checker</h1>
        <br/>
        <hr/>
        <br/>
      <table>
          <thead>
            <tr>
              <td>Relevant</td>
              <td>Date</td>
              <td>Description</td>
              <td>url</td>

            </tr>
          </thead>
          <tbody>
              {% for tweet in TweetsForm.tweets %}
            <tr>
              <td><input name="tablesel-row-{{loop.index}}" type="checkbox" value="on"/></td>
              <td>{{tweet.created_at}}</td>
              <td>{{tweet.text}}</td>
              <td>{{tweet.url}}</td>
            </tr>
              {% endfor %}
          </tbody>
      </table>
    <span>
        <button type="reset">Reset</button>
        <button name="register_button" type="action">Register</button>
    </span>

    </form>
</messageML>
"""


class Response(IResponse):

    def __init__(self, bot_client, next_controller):
        self._bot_client = bot_client
        self._next_controller = next_controller
        self._elements_parser = SymElementsParser()

    def update(self, action):
        button = self._elements_parser.get_action(action)
        if button == "register_button":
            vals = self._elements_parser.get_form_values(action)
            # {'action': 'register_button', 'tablesel-row-3': 'on', 'tablesel-row-4': 'on'}
            msg = dict(message=self._next_controller.render(vals))
            streamId = self._elements_parser.get_stream_id(action)
            mc = self._bot_client.get_message_client()
            mc.send_msg(streamId, msg)


class Controller(GeneralController):

    def __init__(self, response, view, gen_tweets=None):
        super().__init__(response, view)
        fname = os.path.join(os.path.dirname(__file__), "..", "resources", "twitter_credentials.json")
        self._gen = gen_tweets or gen_from_twitter(fname)

    @property
    def responds_to(self):
        return "/strep tweets"

    def render(self, message):
        form_j = super().render(message)

        # message:
        # {'action': 'check_button',
        #  'trade_date': '12/09/2019',
        #  'trade_ticker': 'NASDAQ:AAPL'}
        dt = datetime.strptime(message['trade_date'], "%d/%m/%Y")
        tkr = message['trade_ticker']
        t = Template(form_j, trim_blocks=True, lstrip_blocks=True)
        try:
            tweets = list(gen_table_rows(dt, self._gen(tkr)))
        except Exception as e:
            logging.error(e)
        data = {"TweetsForm": {"form_id": self.make_form_id(self.responds_to),
                               "tweets": tweets}}

        return t.render(data)
