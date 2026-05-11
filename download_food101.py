import shutil
from pathlib import Path

import kagglehub

from config import DATASET_DIR, IMAGE_EXTENSIONS, REQUIRED_CLASSES

DATASET_SLUG = "dansbecker/food-101"

CLASS_MAP = {
    "hamburger": "burger",
    "pizza": "pizza",
    "fried_rice": "fried_rice",
    "caesar_salad": "salad",
}

MAX_IMAGES_PER_CLASS = 120


def find_images_root(download_path: Path) -> Path:
    candidates = [
        download_path / "food-101" / "food-101" / "images",
        download_path / "food-101" / "images",
        download_path / "images",
    ]

    for candidate in candidates:
        if candidate.exists():
            return candidate

    matches = [path for path in download_path.rglob("images") if path.is_dir()]
    if matches:
        return matches[0]

    raise SystemExit(f"Could not find Food-101 images folder inside {download_path}")


def copy_class(source_dir: Path, target_dir: Path) -> int:
    target_dir.mkdir(parents=True, exist_ok=True)
    copied = 0

    for image_path in sorted(source_dir.iterdir()):
        if image_path.suffix.lower() not in IMAGE_EXTENSIONS:
            continue
        if copied >= MAX_IMAGES_PER_CLASS:
            break

        target_path = target_dir / f"{source_dir.name}_{copied + 1:04d}{image_path.suffix.lower()}"
        shutil.copy2(image_path, target_path)
        copied += 1

    return copied


def main() -> None:
    download_path = Path(kagglehub.dataset_download(DATASET_SLUG))
    images_root = find_images_root(download_path)
    print(f"Downloaded Food-101 to: {download_path}")
    print(f"Using images folder: {images_root}")
    print()

    for source_class, target_class in CLASS_MAP.items():
        source_dir = images_root / source_class
        if not source_dir.exists():
            print(f"Missing Food-101 class: {source_class}")
            continue

        count = copy_class(source_dir, DATASET_DIR / target_class)
        print(f"Copied {count} images: {source_class} -> model/dataset/{target_class}")

    remaining_classes = [name for name in REQUIRED_CLASSES if name not in CLASS_MAP.values()]
    print()
    print("Food-101 only fills some classes.")
    print("Add these remaining classes manually from other datasets or your own images:")
    for class_name in remaining_classes:
        print(f"- {class_name}")


if __name__ == "__main__":
    main()
