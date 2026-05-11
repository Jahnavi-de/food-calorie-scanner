# Model

This folder contains the CNN model code used by the FastAPI backend.

## Dataset

Put food images inside `model/dataset`, one folder per class:

```text
model/dataset/
  banana/
  bread/
  burger/
  chapati/
  fried_rice/
  grapes/
  idli/
  pizza/
  salad/
  samosa/
  watermelon/
```

These are the only 11 trainable classes. Do not create a folder for `unknown_food`; the app uses `unknown_food` only during inference when CNN confidence is low.

Use at least 50 images per class. For better accuracy, use 100-200+ images per class. Keep the dataset balanced, meaning each class should have roughly the same number of images.

## Train

Run from the project root:

```powershell
python model/train.py
```

## Download Food-101 Classes

Food-101 can fill some project classes such as `pizza`, `burger`, `fried_rice`, and `salad`.

Run:

```powershell
python model\download_food101.py
```

This downloads `dansbecker/food-101` using KaggleHub and copies selected classes into `model/dataset`.
It only fills `burger`, `pizza`, `fried_rice`, and `salad`. Add `banana`, `bread`, `chapati`, `grapes`, `idli`, `samosa`, and `watermelon` manually from other datasets or your own images.

## Download Hugging Face Indian Food Classes

This is the better option for the Indian/common food classes because it streams only the needed images instead of downloading a huge archive first.

Run from the project root:

```powershell
python model/download_hf_indian_food.py
```

It can fill:

```text
burger
bread
chapati
fried_rice
idli
pizza
samosa
```

You still need to add these manually or from a fruit dataset:

```text
banana
grapes
salad
watermelon
```

## Download Kaggle Fruit Classes

For `banana`, `grapes`, `watermelon`, and some `salad` images, run:

```powershell
python model/download_kaggle_fruits.py
```

This uses KaggleHub with `kritikseth/fruit-and-vegetable-image-recognition`.

Training saves:

```text
model/artifacts/food_cnn.keras
model/artifacts/class_names.json
```

## Backend Connection

The FastAPI backend loads `model/inference.py`. It uses the CNN only after both files exist:

```text
model/artifacts/food_cnn.keras
model/artifacts/class_names.json
```

If those files do not exist, the backend uses its demo fallback.
