import json
from datetime import datetime
from sys import stdin, stdout
from parse.Parser import Parser


class Bot(object):

    def __init__(self, seeded_json):
        self.seeded_json = seeded_json
        self.parser = Parser(seeded_json)

    def run(self):
        while not stdin.closed:
            try:
                message = stdin.readline().strip()

                if len(message) == 0:
                    continue

                if self.parser.process(message):
                    self.__respond(self.parser.response())

            except (EOFError, KeyboardInterrupt):
                return

    def __respond(self, response):
        stdout.write(response + '\n')
        stdout.flush()

if __name__ == '__main__':
    with open('seed.txt') as json_data:
        #print json_data
        start_time = datetime.now()
        seeded_data = json.load(json_data)
        end_time = datetime.now()
        #print ("time diff: " + str(end_time-start_time))
    Bot(seeded_data).run()
