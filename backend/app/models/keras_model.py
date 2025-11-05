import tensorflow as tf
from PIL import Image
import numpy as np
from io import BytesIO
import os


class BrainTumorKerasModel:
    def __init__(self, model_path):
        self.model = tf.keras.models.load_model(model_path)

    def preprocess(self, image_bytes):
        image = Image.open(BytesIO(image_bytes)).convert("RGB")
        image = image.resize((128, 128))  # Adjust to your model's input size
        arr = np.array(image) / 255.0     # Normalize; adjust if needed
        arr = arr.astype(np.float32)
        arr = np.expand_dims(arr, axis=0) # Add batch dimension
        return arr

    def predict(self, image_bytes):
        x = self.preprocess(image_bytes)
        preds = self.model.predict(x)
        # Adjust below based on your model output (binary/class/softmax/sigmoid)
        # Example for binary classification: sigmoid output
        prob = float(preds[0][0])
        result = "Yes" if prob >= 0.5 else "No"
        confidence = prob if result == "Yes" else 1 - prob
        return {
            "result": result,
            "confidence": confidence
        }

# Load your model at startup
MODEL_PATH = os.path.join(os.path.dirname(__file__), "brain_tumor_model.h5")
brain_tumor_model = BrainTumorKerasModel(MODEL_PATH)

