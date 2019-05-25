from yapsy.IPlugin import IPlugin
from urllib.request import urlopen
import json

class JeopardyPlugin(IPlugin):
    def process(self, msg, client):
        if ("!jeopardy" in msg['text']):
            response = urlopen('http://jservice.io/api/random?count=1')
            js = json.load(response)
            self.answer = js[0]['answer']
            question = js[0]['question']
            category = js[0]['category']['title']
            response = f"{category}:\n{question}"
            client.send_message(response)

        elif ("!answer" in msg['text']):
            client.send_message(response)
