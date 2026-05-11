import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

from app.ml.food_data import FOOD_CLASSES, get_food_details

PROJECT_ROOT = Path(__file__).resolve().parents[3]
MODEL_PACKAGE = PROJECT_ROOT / "model"
if str(MODEL_PACKAGE) not in sys.path:
    sys.path.insert(0, str(MODEL_PACKAGE))

try:
    from inference import FoodCNN
except Exception:
    FoodCNN = None

MODEL_PATH = PROJECT_ROOT / "model" / "artifacts" / "food_cnn.keras"
CLASS_NAMES_PATH = PROJECT_ROOT / "model" / "artifacts" / "class_names.json"
IMAGE_SIZE = (224, 224)


class FoodPredictor:
    def __init__(self) -> None:
        self.model = None
        self.model_ready = False
        self.class_names = FOOD_CLASSES
        self.cnn = None
        self._load_model()

    def _load_model(self) -> None:
        if FoodCNN is None or not MODEL_PATH.exists() or not CLASS_NAMES_PATH.exists():
            return

        try:
            self.cnn = FoodCNN(MODEL_PATH, CLASS_NAMES_PATH)
            self.model_ready = self.cnn.ready
        except Exception:
            self.cnn = None
            self.model_ready = False

    def predict(self, image: Image.Image) -> dict:
        image = image.convert("RGB")
        if self.model_ready and self.cnn is not None:
            return self.cnn.predict(image)
        return self._predict_with_image_stats(image)

    def _predict_with_cnn(self, image: Image.Image) -> dict:
        resized = image.resize(IMAGE_SIZE)
        arr = np.asarray(resized, dtype=np.float32) / 255.0
        batch = np.expand_dims(arr, axis=0)
        scores = self.model.predict(batch, verbose=0)[0]
        index = int(np.argmax(scores))
        confidence = float(scores[index])
        food_name = self.class_names[index]
        return self._format_prediction(food_name, confidence, "cnn")

    def _predict_with_image_stats(self, image: Image.Image) -> dict:
        """A deterministic fallback used before a trained CNN file exists."""
        thumb = image.resize((96, 96))
        arr = np.asarray(thumb, dtype=np.float32) / 255.0
        red, green, blue = arr[..., 0].mean(), arr[..., 1].mean(), arr[..., 2].mean()
        brightness = arr.mean()
        saturation = (arr.max(axis=2) - arr.min(axis=2)).mean()
        max_channel = arr.max(axis=2)
        min_channel = arr.min(axis=2)
        pixel_saturation = max_channel - min_channel

        red_fruit_pixels = (
            (arr[..., 0] > 0.50)
            & (arr[..., 0] > arr[..., 1] * 1.25)
            & (arr[..., 0] > arr[..., 2] * 1.25)
            & (pixel_saturation > 0.18)
        )
        yellow_fruit_pixels = (
            (arr[..., 0] > 0.50)
            & (arr[..., 1] > 0.42)
            & (arr[..., 2] < 0.35)
            & (pixel_saturation > 0.15)
        )
        dark_grape_pixels = (
            (arr[..., 2] > arr[..., 1] * 1.05)
            & (arr[..., 0] > arr[..., 1] * 0.85)
            & (brightness < 0.48)
        )
        fried_golden_pixels = (
            (arr[..., 0] > 0.46)
            & (arr[..., 1] > 0.28)
            & (arr[..., 1] < 0.72)
            & (arr[..., 2] < 0.36)
            & (arr[..., 0] > arr[..., 1] * 1.08)
            & (arr[..., 1] > arr[..., 2] * 1.35)
            & (pixel_saturation > 0.16)
        )

        red_ratio = float(red_fruit_pixels.mean())
        yellow_ratio = float(yellow_fruit_pixels.mean())
        grape_ratio = float(dark_grape_pixels.mean())
        fried_ratio = float(fried_golden_pixels.mean())
        fruit_score = red_ratio + yellow_ratio + grape_ratio
        bread_like = (
            brightness > 0.45
            and red > green > blue
            and grape_ratio < 0.025
            and fried_ratio > 0.12
            and saturation < 0.30
        )

        if fried_ratio > 0.14 and brightness < 0.48:
            food_name = "samosa"
        elif bread_like:
            food_name = "bread"
        elif red_ratio > 0.10 and (grape_ratio > 0.025 or yellow_ratio > 0.06):
            food_name = "fruit_plate"
        elif red_ratio > 0.12 and green < red * 0.82:
            food_name = "watermelon"
        elif grape_ratio > 0.08:
            food_name = "grapes"
        elif yellow_ratio > 0.12:
            food_name = "banana"
        elif green > red and green > blue and brightness > 0.45:
            food_name = "salad"
        elif red > 0.58 and green < 0.48:
            food_name = "pizza"
        elif brightness > 0.72 and saturation < 0.22:
            food_name = "idli"
        elif red > green > blue and brightness < 0.52 and fruit_score < 0.08:
            food_name = "samosa"
        elif red > 0.50 and green > 0.42 and blue < 0.36:
            food_name = "fried_rice"
        elif red > 0.45 and green > 0.38 and blue > 0.30:
            food_name = "burger"
        elif green > 0.45 and red > 0.45 and blue < 0.35:
            food_name = "banana"
        else:
            food_name = "chapati"

        confidence = min(0.89, max(0.45, float(abs(red - green) + saturation + fruit_score + 0.38)))
        if food_name == "fruit_plate":
            confidence = max(confidence, 0.72)
        if confidence < 0.50:
            food_name = "unknown_food"
        return self._format_prediction(food_name, confidence, "image-stat-fallback")

    def _format_prediction(self, food_name: str, confidence: float, model_type: str) -> dict:
        details = get_food_details(food_name)
        return {
            "food": food_name,
            "serving": details["serving"],
            "calories": details["calories"],
            "confidence": round(confidence, 3),
            "model_type": model_type,
        }
