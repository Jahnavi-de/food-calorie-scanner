from pathlib import Path

MODEL_ROOT = Path(__file__).resolve().parent
DATASET_DIR = MODEL_ROOT / "dataset"
ARTIFACTS_DIR = MODEL_ROOT / "artifacts"
MODEL_PATH = ARTIFACTS_DIR / "food_cnn.keras"
CLASS_NAMES_PATH = ARTIFACTS_DIR / "class_names.json"
IMAGE_SIZE = (224, 224)
BATCH_SIZE = 16
EPOCHS = 25
MIN_IMAGES_PER_CLASS = 50

REQUIRED_CLASSES = [
    "banana",
    "bread",
    "burger",
    "chapati",
    "fried_rice",
    "grapes",
    "idli",
    "pizza",
    "salad",
    "samosa",
    "watermelon",
]

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
