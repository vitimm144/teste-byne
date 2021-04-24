import requests
import pika
from datetime import datetime
import json


class MultiplyService(object):
    def __init__(self, host) -> None:
        credentials = pika.PlainCredentials('rabbitmq', 'rabbitmq')
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host, credentials=credentials)
        )
        self.channel = self.connection.channel()
        self.routing_key = "multiply_queue"
        self.channel.queue_declare(queue=self.routing_key, durable=True)
        
    def publish(self, number: int):
        data = {
            "number": number,
            "timestamp": datetime.now().timestamp()
        }
        print(f"publishing number {number}")
        self.channel.basic_publish(
            exchange="",
            routing_key=self.routing_key,
            body=json.dumps(data),
            properties=pika.BasicProperties(delivery_mode=2)
        )
        
    @staticmethod
    def get_service_number(url):
        response = requests.get(url)
        number = response.json()
        return number

class Multiply(object):

    def __init__(self, even_url:str, odd_url: str, multiply_service: MultiplyService) -> None:
        self.even_url = even_url
        self.odd_url = odd_url
        self.multiply_service = multiply_service 

    def multiply(self):
        even_number = self.multiply_service.get_service_number(self.even_url)
        odd_number = self.multiply_service.get_service_number(self.odd_url)
        return odd_number.get("number") * even_number.get("number")

    def publisher(self):
        number = self.multiply()
        if number > 10000:
            self.multiply_service.publish(number)
