import numpy as np
import cv2
from PIL import Image
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import easyocr

app = Flask(__name__)

# Initialize EasyOCR reader once
reader = easyocr.Reader(['en'], gpu=False)

@app.route("/ocr", methods=["POST"])
def get_ocr_data():
    print('inside ocr api')
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    file_bytes = uploaded_file.read()
    text_output = ""

    try:
        img = cv2.imdecode(np.frombuffer(file_bytes, np.uint8), cv2.IMREAD_COLOR)
        if img is None:
            return jsonify({"error": "Failed to decode image."}), 400

        # Convert to RGB and run OCR
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = reader.readtext(img_rgb)

        text_output = " ".join([res[1] for res in results])

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"text": text_output.strip()})

if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")
