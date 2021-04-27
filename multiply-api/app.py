from datetime import datetime
from mongoengine import connect
from autobahn.wamp.types import ComponentConfig
import json
from twisted.internet.defer import inlineCallbacks
from services import NumberService, ApiService
from autobahn.twisted.component import run
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from autobahn import wamp
from autobahn.twisted.util import sleep
from twisted.internet import reactor



connect(host= "mongodb://mongo_admin:mongo_passwd@mongo:27017/byne?authSource=admin")


class MultiplySession(ApplicationSession):
    numberService = None

    def __init__(self, config):
        ApplicationSession.__init__(self, config=config)
        self.numberService = NumberService()
    
    def onConnect(self):
        print('transport connected')

        # lets join a realm .. normally, we would also specify
        # how we would like to authenticate here
        self.join(self.config.realm)

    @inlineCallbacks
    def onJoin(self, details):
        print("session attached")
        try:
            yield self.register(self.get_numbers, 'api.get_numbers')
            yield self.register(self.api_ping, 'api.ping')
        except Exception as e:
            print(e)
        reactor.callInThread(self.connect_rabbit)
        

    def get_numbers(self):
        result = self.numberService.get()
        print('api.get_numbers')
        print(result)
        return result
    
    def api_ping(self):
        print('pong')
        return {
            "data": "pong"
        }

    
    def connect_rabbit(self):
        try:
            api_service = ApiService("rabbit", "multiply_queue", self.numberService)
            api_service.run()
        except Exception as e:
            print(e)
            sleep(5)
            self.connect_rabbit()


if __name__ == "__main__":
    url =  u"ws://127.0.0.1:8000/ws"
    realm = u"realm1"
    # session = MultiplySession(ComponentConfig(realm, {}))
    runner = ApplicationRunner(url=url, realm=realm)
    runner.run(MultiplySession, start_reactor=True)
    