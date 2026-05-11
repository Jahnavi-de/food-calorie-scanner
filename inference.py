import json
from pathlib import Path

import numpy as np
from PIL import Image

from config import CLASS_NAMES_PATH, IMAGE_SIZE, MODEL_PATH
from food_info import food_details

CONFIDENCE_THRESHOLD = 0.60
TOP_K = 3


class FoodCNN:
    def __init__(
        self,
        model_path: Path = MODEL_PATH,
        class_names_path: Path = CLASS_NAMES_PATH,
    ) -> None:
        self.model_path = model_path
        self.class_names_path = class_names_path
        self.model = None
        self.class_names: list[str] = []
        self.ready = False
        self.load()

    def load(self) -> None:
        if not self.model_path.exists() or not self.class_names_path.exists():
            return

        from tensorflow import keras

        self.model = keras.models.load_model(self.model_path)
        self.class_names = json.loads(self.class_names_path.read_text(encoding="utf-8"))
        self.ready = True

    def predict(self, image: Image.Image) -> dict:
        if not self.ready or self.model is None:
            raise RuntimeError("Trained model not found. Run: python model/train.py")

        image = image.convert("RGB").resize(IMAGE_SIZE)
        arr = np.asarray(image, dtype=np.float32)
        batch = np.expand_dims(arr, axis=0)
        scores = self.model.predict(batch, verbose=0)[0]
        top_indices = np.argsort(scores)[-TOP_K:][::-1]
        top_predictions = [
            {
                "food": self.class_names[int(index)],
                "confidence": round(float(scores[int(index)]), 3),
            }
            for index in top_indices
        ]

        index = int(top_indices[0])
        confidence = float(scores[index])
        food_name = self.class_names[index]
        if confidence < CONFIDENCE_THRESHOLD:
            food_name = "unknown_food"

        details = food_details(food_name)

        return {
            "food": food_name,
            "serving": details["serving"],
            "calories": details["calories"],
            "confidence": round(confidence, 3),
            "model_type": "cnn",
            "top_predictions": top_predictions,
        }
