from datetime import datetime
from mongoengine import connect
import json
from twisted.internet.defer import inlineCallbacks
from services import NumberService, ApiService
from autobahn.twisted.component import run
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from autobahn import wamp
from autobahn.twisted.util import sleep


connect(host= "mongodb://mongo_admin:mongo_passwd@mongo:27017/byne?authSource=admin")


class MultiplySession(ApplicationSession):
    numberService = None

    def __init__(self, config):
        self.numberService = NumberService()
        super().__init__(config=config)

    @inlineCallbacks
    def onJoin(self, details):
        print("session attached")
        yield self.connect_rabbit()
        

    @wamp.register('api.get_numbers')
    def get_numbers(self):
        result = self.numberService.get()
        return {
            "data": list(result)
        }

    @inlineCallbacks
    def connect_rabbit(self):
        try:
            api_service = yield ApiService("rabbit", "multiply_queue", self.numberService)
            yield api_service.run()
        except Exception as e:
            print(e)
            yield sleep(5)
            yield self.connect_rabbit()


if __name__ == "__main__":
    url =  "ws://127.0.0.1:8000/ws"
    realm = "realm1"
    runner = ApplicationRunner(url, realm)
    runner.run(MultiplySession)
    