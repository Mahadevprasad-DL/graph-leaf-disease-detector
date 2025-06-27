from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image as keras_image
import numpy as np
import os

app = Flask(__name__)

# Load your trained grape leaf disease model
model = load_model('grape_disease_model.h5')

# Load general classifier (MobileNetV2) for leaf detection
mobilenet_model = MobileNetV2(weights='imagenet')

# Classes and corresponding cure suggestions
classes = ['Black Rot', 'Esca (Black Measles)', 'Leaf Blight', 'Healthy']
cures = {
    'Black Rot': 'Remove infected leaves and apply fungicide like Mancozeb.',
    'Esca (Black Measles)': 'Prune affected vines and avoid overwatering.',
    'Leaf Blight': 'Use copper-based fungicides and ensure proper air circulation.',
    'Healthy': 'No disease detected. Maintain regular vineyard monitoring.'
}

# File upload settings
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

CONFIDENCE_THRESHOLD = 75  # Adjust this if needed


# 🧠 Detect if uploaded image is likely a leaf using MobileNetV2
def is_leaf_image(image_path, top_k=5):
    try:
        img = keras_image.load_img(image_path, target_size=(224, 224))
        img_array = keras_image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)

        preds = mobilenet_model.predict(img_array)
        decoded_preds = decode_predictions(preds, top=top_k)[0]

        print("🔍 MobileNet Predictions:")
        for _, label, prob in decoded_preds:
            print(f"→ {label} ({prob * 100:.2f}%)")

        # Expanded keywords to cover more leaf-like classes
        leaf_keywords = [
            'leaf', 'plant', 'tree', 'foliage', 'flower',
            'vegetation', 'herb', 'shrub', 'vine',
            'maize', 'corn', 'banana', 'sunflower', 'potato',
            'cabbage', 'lettuce', 'grape'
        ]

        for _, label, _ in decoded_preds:
            if any(keyword in label.lower() for keyword in leaf_keywords):
                return True
        return False
    except Exception as e:
        print(f"Error in is_leaf_image: {e}")
        return False


# Main route
@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    image_url = None
    error = None
    cure = None
    confidence = None

    if request.method == 'POST':
        file = request.files['image']
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        image_url = filepath

        # Use MobileNetV2 to verify it's a plant/leaf
        if not is_leaf_image(filepath):
            error = "This image doesn't seem to contain a grape leaf. Please upload a clear leaf image."
            return render_template('index.html', result=result, image_url=image_url, error=error, cure=cure, confidence=confidence)

        try:
            # Preprocess image for grape disease model
            img = load_img(filepath, target_size=(150, 150))
            img_array = img_to_array(img) / 255.0
            img_array = np.expand_dims(img_array, axis=0)

            prediction = model.predict(img_array)[0]
            confidence = round(100 * np.max(prediction), 2)

            if confidence < CONFIDENCE_THRESHOLD:
                error = "This image doesn't appear to be a grape leaf. Please upload a clear leaf image."
            else:
                predicted_class = classes[np.argmax(prediction)]
                result = f"{predicted_class} ({confidence}%)"
                cure = cures[predicted_class]

        except Exception:
            error = "Error processing image. Please upload a valid image."

    return render_template('index.html', result=result, image_url=image_url, error=error, cure=cure, confidence=confidence)


if __name__ == '__main__':
    app.run(debug=True)
