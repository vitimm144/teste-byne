import pika
import json
import json
from pika.adapters.twisted_connection import TwistedProtocolConnection
from models import Number
from abc import ABC, abstractmethod
from repositories import INumberRepository, INumber
from datetime import datetime
from mongoengine import connect


class NumberServiceMongo(INumberRepository):

    def __init__(self) -> None:
        self.connect()

    @staticmethod
    def save(data: INumber):
        number = Number(
            number = data.number,
            timestamp = data.timestamp
        )
        number.save()

    @staticmethod
    def get():
        data = []
        queryset = Number.objects().order_by('-timestamp')[:100]
        if queryset:
            data = json.loads(queryset.to_json())
        return data
    
    @staticmethod
    def connect():
        connect(host="mongodb://mongo_admin:mongo_passwd@mongo:27017/byne?authSource=admin")

class IApiService(ABC):
    @abstractmethod
    def run():
        pass

    @abstractmethod
    def on_message():
        pass


class ApiServiceRabbitMQ(IApiService):
    def __init__(self, host: str, queue: str, number_service: INumberRepository ) -> None:
        self.number_service = number_service
        credentials = pika.PlainCredentials('rabbitmq', 'rabbitmq')
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host, credentials=credentials)
        )
        self.channel = self.connection.channel()
        self.queue = queue
        self.channel.basic_consume(self.queue, self.on_message)
    
    def run(self):
        self.channel.start_consuming()

    def on_message(self, chan, method_frame, header, body):
        data = json.loads(body)
        number = INumber(
            data.get('number'),
            datetime.fromtimestamp(data.get("timestamp"))
        )
        self.number_service.save(number) 
        chan.basic_ack(delivery_tag=method_frame.delivery_tag)
