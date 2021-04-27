import os
from multiply import MultiplyService, Multiply
from twisted.internet import reactor, task
from dotenv import load_dotenv


load_dotenv()


if __name__ == "__main__":
    multiply_service = MultiplyService(
        os.environ.get("MULTIPLY_SV_HOST", "rabbit"),
        os.environ.get("MULTIPLY_SV_USER","rabbitmq"),
        os.environ.get("MULTIPLY_SV_PASS","rabbitmq")
    )
    multiply = Multiply(
        os.environ.get("EVEN_SERVICE_URL", "http://even-service:5000/even_service/number"),
        os.environ.get("ODD_SERVICE_URL","http://odd-service:5001/odd_service/number"),
        multiply_service
    )
    task = task.LoopingCall(multiply.publisher)
    task.start(0.5)
    reactor.run()
    
    