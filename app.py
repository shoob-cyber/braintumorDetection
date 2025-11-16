from flask import Flask, request, jsonify, render_template
import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
import cv2
from PIL import Image
import io

app = Flask(__name__)

# Load the trained model
MODEL_PATH = 'model/brain_tumor_model.h5'
model = load_model(MODEL_PATH)

# Define the class labels in the correct order
CLASS_LABELS = ['glioma_tumor', 'meningioma_tumor', 'no_tumor', 'pituitary_tumor']

# Information Dictionary (FOR EDUCATIONAL PURPOSES ONLY)
INFO_DICT = {
    'glioma_tumor': {
        'specialist': 'Neuro-Oncologist or Neurosurgeon',
        'info': 'Gliomas are tumors from glial cells in the brain. Treatment often involves surgery, radiation, and chemotherapy.'
    },
    'meningioma_tumor': {
        'specialist': 'Neurosurgeon or Neurologist',
        'info': 'Meningiomas arise from the membranes surrounding the brain. Many are benign. Treatment may involve observation, surgery, or radiation.'
    },
    'pituitary_tumor': {
        'specialist': 'Endocrinologist or Neurosurgeon',
        'info': 'Pituitary tumors develop in the pituitary gland and can affect hormone levels. Treatment includes surgery, medication, or radiation.'
    },
    'no_tumor': {
        'specialist': 'N/A',
        'info': 'The model did not detect a tumor. This is not a medical diagnosis. Always consult a doctor for a definitive evaluation.'
    }
}

def preprocess_image(image, target_size=(150, 150)):
    """Preprocesses the image for the model."""
    img = np.array(image)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    img = cv2.resize(img, target_size)
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    return img

@app.route('/', methods=['GET'])
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Handle the image prediction request."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        image_bytes = file.read()
        image = Image.open(io.BytesIO(image_bytes))
        
        processed_image = preprocess_image(image)
        prediction = model.predict(processed_image)
        
        predicted_class_index = np.argmax(prediction, axis=1)[0]
        predicted_class_label = CLASS_LABELS[predicted_class_index]
        confidence = float(np.max(prediction)) * 100
        
        result_info = INFO_DICT[predicted_class_label]

        return jsonify({
            'prediction': predicted_class_label.replace('_', ' ').title(),
            'confidence': confidence,
            'specialist': result_info['specialist'],
            'info': result_info['info']
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)