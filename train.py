import json

from config import (
    ARTIFACTS_DIR,
    BATCH_SIZE,
    CLASS_NAMES_PATH,
    DATASET_DIR,
    EPOCHS,
    IMAGE_EXTENSIONS,
    IMAGE_SIZE,
    MIN_IMAGES_PER_CLASS,
    MODEL_PATH,
    REQUIRED_CLASSES,
)


def count_images(class_name: str) -> int:
    class_dir = DATASET_DIR / class_name
    if not class_dir.exists():
        return 0

    return sum(1 for item in class_dir.iterdir() if item.suffix.lower() in IMAGE_EXTENSIONS)


def validate_dataset() -> list[str]:
    if not DATASET_DIR.exists():
        raise SystemExit(f"Dataset folder missing: {DATASET_DIR}")

    print("Dataset check")
    print(f"Dataset folder: {DATASET_DIR}")
    print(f"Required images per class: {MIN_IMAGES_PER_CLASS}")
    print()

    existing_class_names = sorted(path.name for path in DATASET_DIR.iterdir() if path.is_dir())
    extra_classes = [
        name
        for name in sorted(set(existing_class_names) - set(REQUIRED_CLASSES))
        if count_images(name) > 0
    ]
    if extra_classes:
        raise SystemExit(
            "Remove or move unsupported class folders before training:\n"
            + "\n".join(f"- {name}" for name in extra_classes)
            + "\n\nThis model trains only these 12 classes:\n"
            + ", ".join(REQUIRED_CLASSES)
        )

    missing_folders = []
    missing = []
    class_counts = {}
    for class_name in REQUIRED_CLASSES:
        class_dir = DATASET_DIR / class_name
        if not class_dir.exists():
            missing_folders.append(class_name)
            image_count = 0
        else:
            image_count = count_images(class_name)

        class_counts[class_name] = image_count
        print(f"{class_name:12} {image_count:4} images")

        if image_count < MIN_IMAGES_PER_CLASS:
            missing.append(f"{class_name}: {image_count} images")

    if missing_folders:
        raise SystemExit(
            "\nCreate these missing class folders inside model/dataset:\n"
            + "\n".join(f"- {name}" for name in missing_folders)
        )

    if missing:
        raise SystemExit(
            f"\nAdd at least {MIN_IMAGES_PER_CLASS} images per class before training.\n"
            + "\n".join(missing)
        )

    max_count = max(class_counts.values())
    min_count = min(class_counts.values())
    if max_count > min_count * 2:
        print()
        print("Warning: dataset is imbalanced.")
        print("Try to keep each class close to the same image count for better accuracy.")

    print()
    print("Dataset is ready.")
    return REQUIRED_CLASSES


def build_model(keras, layers, class_count: int):
    augmentation = keras.Sequential(
        [
            layers.RandomFlip("horizontal"),
            layers.RandomRotation(0.08),
            layers.RandomZoom(0.12),
            layers.RandomContrast(0.12),
        ],
        name="augmentation",
    )

    base_model = keras.applications.MobileNetV2(
        input_shape=(*IMAGE_SIZE, 3),
        include_top=False,
        weights="imagenet",
    )
    base_model.trainable = False

    inputs = keras.Input(shape=(*IMAGE_SIZE, 3))
    x = augmentation(inputs)
    x = keras.applications.mobilenet_v2.preprocess_input(x)
    x = base_model(x, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dropout(0.3)(x)
    x = layers.Dense(128, activation="relu")(x)
    outputs = layers.Dense(class_count, activation="softmax")(x)

    model = keras.Model(inputs, outputs)
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.0005),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model


def main() -> None:
    class_names = validate_dataset()

    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras import layers

    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    CLASS_NAMES_PATH.write_text(json.dumps(class_names, indent=2), encoding="utf-8")

    train_ds = keras.utils.image_dataset_from_directory(
        DATASET_DIR,
        class_names=class_names,
        validation_split=0.2,
        subset="training",
        seed=42,
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
    )
    val_ds = keras.utils.image_dataset_from_directory(
        DATASET_DIR,
        class_names=class_names,
        validation_split=0.2,
        subset="validation",
        seed=42,
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
    )

    train_ds = train_ds.cache().shuffle(512).prefetch(tf.data.AUTOTUNE)
    val_ds = val_ds.cache().prefetch(tf.data.AUTOTUNE)

    model = build_model(keras, layers, len(class_names))
    callbacks = [
        keras.callbacks.EarlyStopping(
            monitor="val_accuracy",
            patience=5,
            mode="max",
            restore_best_weights=True,
            verbose=1,
        ),
        keras.callbacks.ModelCheckpoint(
            filepath=MODEL_PATH,
            monitor="val_accuracy",
            mode="max",
            save_best_only=True,
            verbose=1,
        ),
    ]

    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=EPOCHS,
        callbacks=callbacks,
    )

    CLASS_NAMES_PATH.write_text(json.dumps(class_names, indent=2), encoding="utf-8")

    print(f"Saved best model: {MODEL_PATH}")
    print(f"Saved class names: {CLASS_NAMES_PATH}")
    print(f"Best validation accuracy: {max(history.history['val_accuracy']):.3f}")


if __name__ == "__main__":
    main()
