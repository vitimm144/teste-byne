from multiply import MultiplyService, Multiply
from twisted.internet import reactor, task


if __name__ == "__main__":
    multiply_service = MultiplyService('rabbit')
    multiply = Multiply(
        "http://even-service:5000/even_service/number",
        "http://odd-service:5001/odd_service/number",
        multiply_service
    )
    task = task.LoopingCall(multiply.publisher)
    task.start(0.5)
    reactor.run()
    
    