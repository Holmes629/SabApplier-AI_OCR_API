from flask import Flask, request, jsonify
from PIL import Image
import pytesseract
import io
import tempfile
from pdf2image import convert_from_bytes

app = Flask(__name__)

@app.route('/ocr', methods=['POST'])
def ocr():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    uploaded_file = request.files['file']
    filename = uploaded_file.filename.lower()
    file_bytes = uploaded_file.read()

    text_output = ""

    try:
        if filename.endswith('.pdf'):
            # Convert PDF to list of images (one per page)
            images = convert_from_bytes(file_bytes)
            for image in images:
                text_output += pytesseract.image_to_string(image) + "\n"
        else:
            # Handle normal image files
            image = Image.open(io.BytesIO(file_bytes))
            text_output = pytesseract.image_to_string(image)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'text': text_output.strip()})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
