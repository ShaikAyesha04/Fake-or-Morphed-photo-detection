from flask import Flask, request, jsonify
from flask_cors import CORS
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from io import BytesIO

app = Flask(__name__)
CORS(app)

# Load your trained model
model = load_model("best_resnet50_model.h5")

@app.route('/')
def home():
    return "Fake Image Detector API is running!"

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    try:
        # Load and preprocess the image
        img = image.load_img(BytesIO(file.read()), target_size=(128, 128))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0

        # Predict using the model
        prediction = model.predict(img_array)[0][0]
        label = "fake" if prediction > 0.5 else "real"

        return jsonify({
            "prediction": label,
            "confidence": float(prediction)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

