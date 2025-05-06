import os
import numpy as np
import cv2
import fitz  # PyMuPDF
from flask import Flask, request, jsonify
from easyocr import Reader
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Initialize EasyOCR with English language
ocr_reader = Reader(['en'], gpu=False)

@app.route("/ocr", methods=["POST"])
def get_ocr_data():
    print('inside get ocr api func...')
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
                    results = ocr_reader.readtext(img)
                    for line in results:
                        text_output += line[1] + " "
        else:
            img = cv2.imdecode(np.frombuffer(file_bytes, np.uint8), cv2.IMREAD_COLOR)
            if img is None:
                return jsonify({"error": "Failed to decode image."}), 400
            results = ocr_reader.readtext(img)
            text_output = " ".join([line[1] for line in results])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"text": text_output.strip()})

if __name__ == "__main__":
    app.run(debug=False, port=os.getenv("PORT", 5000), host="0.0.0.0")
