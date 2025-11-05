from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import io
import os

# Load the model from the same folder as this file
MODEL_FILENAME = "brain_hemorrhage.h5"
model_path = os.path.join(os.path.dirname(__file__), MODEL_FILENAME)
model = load_model(model_path)

def preprocess_image(contents):
    img = Image.open(io.BytesIO(contents)).convert("RGB")
    img = img.resize((224, 224))   # adjust if needed for your model
    x = np.array(img) / 255.0
    x = np.expand_dims(x, 0)
    return x

def predict(contents):
    x = preprocess_image(contents)
    pred = model.predict(x)[0]
    label, confidence = ("Yes", float(pred[0])) if pred[0] > 0.5 else ("No", 1.0 - float(pred[0]))
    return {"result": label, "confidence": confidence}
