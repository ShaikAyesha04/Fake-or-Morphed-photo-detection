# Fake or Morphed Photo Detection 🕵️‍♀️🖼️

This project uses a deep learning model based on **ResNet** to detect whether an image is real, fake, or morphed. It features a simple web interface where users can upload images and get a prediction with confidence scores.

## 🚀 Features
- Upload images and detect morphing/fake content
- Uses a pretrained **ResNet** deep learning model for feature extraction
- Flask backend for processing and prediction
- HTML/CSS frontend with file upload and result display

## 🧠 ML Model
- **Architecture**: ResNet (Residual Neural Network)
- **Framework**: PyTorch (or TensorFlow, depending on what you used)
- **Input**: Image file (JPG/PNG)
- **Output**: "Real", "Fake", or "Morphed" label with confidence

## 🛠️ Tech Stack
- **Frontend**: HTML, CSS, Bootstrap
- **Backend**: Python with Flask
- **Model**: ResNet-based CNN
- **Others**: Git, GitHub


## 🔧 How to Run Locally
```bash
# Clone the repository
git clone https://github.com/ShaikAyesha04/Fake-or-Morphed-photo-detection.git
cd Fake-or-Morphed-photo-detection

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py

