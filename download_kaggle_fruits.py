import shutil
from pathlib import Path

import kagglehub

from config import DATASET_DIR, IMAGE_EXTENSIONS, MIN_IMAGES_PER_CLASS

DATASET_SLUG = "kritikseth/fruit-and-vegetable-image-recognition"

CLASS_MAP = {
    "banana": "banana",
    "grapes": "grapes",
    "watermelon": "watermelon",
    "lettuce": "salad",
    "cabbage": "salad",
}

MAX_IMAGES_PER_CLASS = 80


def normalize_name(name: str) -> str:
    return name.strip().lower().replace(" ", "_").replace("-", "_")


def existing_image_count(folder: Path) -> int:
    if not folder.exists():
        return 0
    return sum(1 for item in folder.rglob("*") if item.suffix.lower() in IMAGE_EXTENSIONS)


def find_class_folders(download_path: Path) -> dict[str, list[Path]]:
    class_folders: dict[str, list[Path]] = {}
    for folder in download_path.rglob("*"):
        if not folder.is_dir():
            continue
        normalized = normalize_name(folder.name)
        if normalized in CLASS_MAP:
            class_folders.setdefault(normalized, []).append(folder)
    return class_folders


def copy_images(source_folder: Path, target_class: str, start_index: int) -> int:
    target_folder = DATASET_DIR / target_class
    target_folder.mkdir(parents=True, exist_ok=True)
    copied = 0

    for image_path in sorted(source_folder.rglob("*")):
        if image_path.suffix.lower() not in IMAGE_EXTENSIONS:
            continue

        next_index = start_index + copied + 1
        target_path = target_folder / f"{target_class}_{next_index:04d}{image_path.suffix.lower()}"
        if target_path.exists():
            continue

        shutil.copy2(image_path, target_path)
        copied += 1

        if start_index + copied >= MAX_IMAGES_PER_CLASS:
            break

    return copied


def main() -> None:
    print(f"Downloading Kaggle dataset: {DATASET_SLUG}", flush=True)
    download_path = Path(kagglehub.dataset_download(DATASET_SLUG))
    print(f"Downloaded to: {download_path}", flush=True)

    class_folders = find_class_folders(download_path)
    counts = {
        "banana": existing_image_count(DATASET_DIR / "banana"),
        "grapes": existing_image_count(DATASET_DIR / "grapes"),
        "watermelon": existing_image_count(DATASET_DIR / "watermelon"),
        "salad": existing_image_count(DATASET_DIR / "salad"),
    }

    for source_class, folders in sorted(class_folders.items()):
        target_class = CLASS_MAP[source_class]
        if counts[target_class] >= MAX_IMAGES_PER_CLASS:
            continue

        for folder in folders:
            if counts[target_class] >= MAX_IMAGES_PER_CLASS:
                break
            copied = copy_images(folder, target_class, counts[target_class])
            counts[target_class] += copied
            if copied:
                print(f"Copied {copied:3} images: {folder.name} -> {target_class}", flush=True)

    print()
    print("Kaggle fruit/vegetable summary")
    for class_name, count in sorted(counts.items()):
        print(f"{class_name:12} {count:4} images")

    print()
    print(f"Training needs at least {MIN_IMAGES_PER_CLASS} images in every required class folder.")


if __name__ == "__main__":
    main()
