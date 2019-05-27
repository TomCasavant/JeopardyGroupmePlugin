from yapsy.IPlugin import IPlugin
from urllib.request import urlopen
import json
import glob, os
from difflib import SequenceMatcher

class JeopardyPlugin(IPlugin):
    def process(self, msg, client):
        if ("!jeopardy" in msg['text']):
            score = False
            question = False
            category = False
            while(not score or not question or not category):
                response = urlopen('http://jservice.io/api/random?count=1')
                js = json.load(response)
                file = open("answer.txt", "w")
                file.write(js[0]['answer'].replace("<i>","").replace("</i>",""))
                file.close()

                file = open("score_to_add.s", "w")
                score = js[0]['value']
                file.write(f"{score}")
                file.close()

                question = js[0]['question']
                category = js[0]['category']['title']
                response = f"{category} ({score}):\n{question}"

            client.send_message(response)

        elif ("!answer" in msg['text']):
            try:
                file = open("answer.txt", "r")
                answer = file.read()
                file.close()
                if (answer != ""):
                    if self.similar(msg['text'][8:], answer) >= .55:
                        response = f"Correct! The answer was {answer}"
                        self.add_score(msg['name'])
                    else:
                        response = f"Incorrect! The answer was {answer}"

                    open("answer.txt", "w").close()
                    client.send_message(response)
                else:
                    raise Error("Answer not created yet")
            except:
                client.send_message("You have to call !jeopardy first")

        elif ("!scores" in msg['text']):
            scores = []
            for file in glob.glob("*.score"):
                name = file.replace(".score","")
                f = open(file, "r")
                score = f.read()
                f.close()
                scores.append((name, score))

            scores.sort(key=self.get_second)
            response = "Jeopardy Scores:\n"
            for score in scores:
                response = response + f"{score[0]}: {score[1]}\n"
            client.send_message(response)

    def get_second(self, elem):
        return elem[1]

    def similar(self, a, b):
        comp1 = a.replace("(","").replace(")","").lower()
        comp2 = b.replace("(","").replace(")","").lower()
        return SequenceMatcher(None, comp1, comp2).ratio()

    def add_score(self, name):
        file = open("score_to_add.s", "r")
        score_to_add = int(file.read())
        file.close()
        try:
            file = open(f"{name}.score", "r+")
            current_score = int(file.read())
            file.close()
        except:
            current_score = 0

        file = open(f"{name}.score", "w")
        file.write(f"{current_score + score_to_add}")
        file.close()