from itertools import chain
from pathlib import Path

from datasets import load_dataset
from PIL import Image

from config import DATASET_DIR, IMAGE_EXTENSIONS, MIN_IMAGES_PER_CLASS, REQUIRED_CLASSES

DATASET_SLUG = "rajistics/indian_food_images"

CLASS_MAP = {
    "burger": "burger",
    "butter_naan": "bread",
    "chapati": "chapati",
    "fried_rice": "fried_rice",
    "idli": "idli",
    "pizza": "pizza",
    "samosa": "samosa",
}

MAX_IMAGES_PER_CLASS = 80


def normalize_label(label: str) -> str:
    return label.strip().lower().replace(" ", "_").replace("-", "_")


def load_streaming_dataset():
    try:
        return load_dataset(DATASET_SLUG, split="train", streaming=True)
    except Exception:
        dataset_dict = load_dataset(DATASET_SLUG, streaming=True)
        first_split_name = next(iter(dataset_dict))
        return dataset_dict[first_split_name]


def find_columns(sample: dict) -> tuple[str, str]:
    image_column = None
    label_column = None

    for key, value in sample.items():
        if key.lower() in {"image", "img"} or isinstance(value, Image.Image):
            image_column = key
        if key.lower() in {"label", "labels", "class", "category"}:
            label_column = key

    if image_column is None:
        raise SystemExit(f"Could not find image column. Sample keys: {list(sample.keys())}")
    if label_column is None:
        raise SystemExit(f"Could not find label column. Sample keys: {list(sample.keys())}")

    return image_column, label_column


def label_to_name(dataset, label_column: str, label_value) -> str:
    feature = dataset.features.get(label_column) if dataset.features else None
    if hasattr(feature, "int2str") and isinstance(label_value, int):
        return normalize_label(feature.int2str(label_value))
    return normalize_label(str(label_value))


def existing_image_count(folder: Path) -> int:
    if not folder.exists():
        return 0
    return sum(1 for item in folder.iterdir() if item.suffix.lower() in IMAGE_EXTENSIONS)


def save_image(image, target_folder: Path, target_class: str, index: int) -> None:
    target_folder.mkdir(parents=True, exist_ok=True)
    target_path = target_folder / f"{target_class}_{index:04d}.jpg"

    if isinstance(image, Image.Image):
        pil_image = image
    elif isinstance(image, dict) and image.get("path"):
        pil_image = Image.open(image["path"])
    else:
        raise ValueError(f"Unsupported image value: {type(image)}")

    pil_image.convert("RGB").save(target_path, "JPEG", quality=92)


def main() -> None:
    print(f"Connecting to Hugging Face dataset: {DATASET_SLUG}", flush=True)
    print("This can take a few minutes the first time.", flush=True)

    dataset = load_streaming_dataset()
    print("Dataset stream opened. Reading first sample...", flush=True)

    iterator = iter(dataset)
    first_sample = next(iterator)
    image_column, label_column = find_columns(first_sample)

    counts = {
        target_class: existing_image_count(DATASET_DIR / target_class)
        for target_class in set(CLASS_MAP.values())
    }

    print(f"Using Hugging Face dataset: {DATASET_SLUG}", flush=True)
    print(f"Image column: {image_column}", flush=True)
    print(f"Label column: {label_column}", flush=True)
    print(f"Saving up to {MAX_IMAGES_PER_CLASS} images per matched class", flush=True)
    print("Matched classes will appear below as images are saved.", flush=True)
    print(flush=True)

    for sample in chain([first_sample], iterator):
        source_label = label_to_name(dataset, label_column, sample[label_column])
        target_class = CLASS_MAP.get(source_label)
        if target_class is None:
            continue
        if counts[target_class] >= MAX_IMAGES_PER_CLASS:
            if all(count >= MAX_IMAGES_PER_CLASS for count in counts.values()):
                break
            continue

        counts[target_class] += 1
        save_image(sample[image_column], DATASET_DIR / target_class, target_class, counts[target_class])

        if counts[target_class] % 10 == 0:
            print(f"{target_class:12} {counts[target_class]} images", flush=True)

    print()
    print("Download/copy summary")
    for target_class in sorted(counts):
        print(f"{target_class:12} {counts[target_class]} images")

    remaining = [class_name for class_name in REQUIRED_CLASSES if class_name not in CLASS_MAP.values()]
    print()
    print("Still add these classes from fruit datasets or your own images:")
    for class_name in remaining:
        print(f"- {class_name}")

    print()
    print(f"Training needs at least {MIN_IMAGES_PER_CLASS} images in every required class folder.")


if __name__ == "__main__":
    main()
