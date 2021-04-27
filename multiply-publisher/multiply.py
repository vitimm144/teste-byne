import requests
import pika
from datetime import datetime
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class INumberDTO:
    number: int
    timestamp: int


class IMultiplyService(ABC): 
    @abstractmethod
    def publish(self, number: int) -> None:
        pass
    
    @abstractmethod
    def get_service_number(url: str) -> INumberDTO:
        pass


class MultiplyService(IMultiplyService):
    def __init__(self, host, user, password) -> None:
        credentials = pika.PlainCredentials(user, password)
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
    def get_service_number(url) -> INumberDTO:
        response = requests.get(url)
        json_response = response.json()
        return INumberDTO(json_response.get('number'), json_response.get('timestamp'))


class Multiply(object):
    def __init__(self, even_url:str, odd_url: str, multiply_service: IMultiplyService) -> None:
        self.even_url = even_url
        self.odd_url = odd_url
        self.multiply_service = multiply_service 

    def multiply(self):
        even_number = self.multiply_service.get_service_number(self.even_url)
        odd_number = self.multiply_service.get_service_number(self.odd_url)
        return odd_number.number * even_number.number

    def publisher(self):
        number = self.multiply()
        if number > 10000:
            self.multiply_service.publish(number)
