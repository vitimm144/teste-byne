import mongoengine

class Number(mongoengine.Document):
    number = mongoengine.IntField()
    timestamp = mongoengine.DateTimeField()