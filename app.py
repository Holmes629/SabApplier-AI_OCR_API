import os
import numpy as np
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/ocr", methods=["POST", "GET"])
def get_ocr_data():
    print('inside get ocr api func...')
    return jsonify({"text": 'successfully executed'})

if __name__ == "__main__":
    app.run(debug=False, port=os.getenv("PORT", 5000), host="0.0.0.0")
