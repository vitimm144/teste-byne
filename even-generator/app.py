from flask import Flask, Response
from flask_cors import CORS
from datetime import datetime
from even import even
import json


app = Flask(__name__)
CORS(app)


@app.route("/even_service/number")
def even_number():
    result = even()
    return Response(
        status=200, 
        response=json.dumps({
            "number": result, "timestamp": datetime.now().timestamp()
        }),
        mimetype="application/json"
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
