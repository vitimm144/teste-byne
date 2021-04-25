import pika
import json
from models import Number
from datetime import datetime


class NumberService():
    @staticmethod
    def save(data: dict):
        number = Number(
            number = data.get("number"),
            timestamp = datetime.fromtimestamp(data.get("timestamp"))
        )
        number.save()

    @staticmethod
    def get():
        data = Number.objects().order_by('-timestamp')[:100]
        return data

class ApiService():
    def __init__(self, host: str, queue: str, number_service: NumberService ) -> None:
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
        print("on_message")
        print(chan)
        print(body)
        data = json.loads(body)
        self.number_service.save(data) 
        chan.basic_ack(delivery_tag=method_frame.delivery_tag)
