from twisted.internet.defer import inlineCallbacks
from services import NumberServiceMongo, ApiServiceRabbitMQ
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from autobahn.twisted.util import sleep
from twisted.internet import reactor



class MultiplySession(ApplicationSession):
    
    def __init__(self, config):
        ApplicationSession.__init__(self, config=config)
        self.repository = NumberServiceMongo()
    
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
        reactor.callInThread(self.connect_api)

    def get_numbers(self):
        result = self.repository.get()
        print('api.get_numbers')
        print(result)
        return result
    
    def api_ping(self):
        print('pong')
        return {
            "data": "pong"
        }
    
    def connect_api(self):
        try:
            api_service = ApiServiceRabbitMQ("rabbit", "multiply_queue", self.repository)
            api_service.run()
        except Exception as e:
            print(e)
            sleep(5)
            self.connect_api()


if __name__ == "__main__":
    url =  u"ws://127.0.0.1:8000/ws"
    realm = u"realm1"
    runner = ApplicationRunner(url=url, realm=realm)
    runner.run(MultiplySession, start_reactor=True)
    