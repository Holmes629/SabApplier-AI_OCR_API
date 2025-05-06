import os
import numpy as np
import cv2
import fitz  # PyMuPDF
from flask import Flask, request, jsonify
from paddleocr import PaddleOCR
from werkzeug.utils import secure_filename

app = Flask(__name__)

ocr = PaddleOCR(use_angle_cls=True, lang='en')  # Using default model to save memory

@app.route("/ocr", methods=["POST"])
def get_ocr_data():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    file_bytes = uploaded_file.read()
    text_output = ""

    try:
        if filename.lower().endswith(".pdf"):
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                pix = page.get_pixmap(dpi=200)
                img = np.frombuffer(pix.tobytes(), dtype=np.uint8)
                img = cv2.imdecode(img, cv2.IMREAD_COLOR)
                if img is not None:
                    result = ocr.ocr(img, cls=True)
                    for line in result[0]:
                        text_output += line[1][0] + " "
        else:
            img = cv2.imdecode(np.frombuffer(file_bytes, np.uint8), cv2.IMREAD_COLOR)
            if img is None:
                return jsonify({"error": "Failed to decode image."}), 400
            result = ocr.ocr(img, cls=True)
            text_output = " ".join([line[1][0] for line in result[0]])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"text": text_output.strip()})

if __name__ == "__main__":
    app.run(debug=False, port=os.getenv("PORT", 5000), host="0.0.0.0")
