```markdown
# 🍽️ Food Calorie Scanner Web App

## 📌 Project Overview

This is a web-based Food Calorie Scanner application that allows users to upload a food image and get calorie-related health insights. The system detects the food item using a trained CNN model, estimates calories, calculates BMI, and gives fitness-style recommendations based on the user's height and weight.

---

## 🚀 Features

* 📷 Upload Food Image
* 🤖 Food Detection using CNN Model
* 🔥 Calorie Estimation
* ⚖️ BMI Calculation
* 🧾 Serving Size Information
* 🏋️ Fitness-Style Recommendation
* 📊 Top 3 Model Predictions for Debugging
* ❓ Returns `unknown_food` when prediction confidence is low
* 🌐 Frontend and Backend API Integration

---

## 🛠️ Tech Stack

* **Frontend:** Next.js, React, TypeScript, CSS
* **Backend:** Python, FastAPI
* **Machine Learning:** TensorFlow, Keras, MobileNetV2 CNN
* **Image Processing:** Pillow, NumPy
* **API Server:** Uvicorn
* **Dataset Sources:** Hugging Face, Kaggle

---

## 🍱 Food Classes

The CNN model is trained on 11 food classes:

```text
banana
bread
burger
chapati
fried_rice
grapes
idli
pizza
salad
samosa
watermelon
```

`unknown_food` is not trained as a class. It is returned only when prediction confidence is below `0.60`.

---

## 📂 Project Structure

```text
food-calorie-scanner/
│
├── frontend/
│   ├── app/
│   │   ├── page.tsx
│   │   ├── layout.tsx
│   │   └── globals.css
│   ├── lib/
│   │   └── api.ts
│   ├── package.json
│   └── next.config.mjs
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   └── ml/
│   │       ├── predictor.py
│   │       ├── recommendation.py
│   │       └── food_data.py
│   └── requirements.txt
│
├── model/
│   ├── config.py
│   ├── train.py
│   ├── inference.py
│   ├── food_info.py
│   ├── download_hf_indian_food.py
│   ├── download_kaggle_fruits.py
│   ├── dataset/
│   └── artifacts/
│
├── README.md
└── .gitignore
```

---

## ⚙️ How It Works

1. User uploads a food image from the frontend
2. User enters height and weight
3. Frontend sends image and user data to FastAPI backend
4. Backend loads the trained CNN model
5. CNN predicts the food class
6. System fetches calories and serving size
7. BMI is calculated using height and weight
8. Fitness-style recommendation is generated
9. Results are displayed on the dashboard

---

## 🧠 Machine Learning Model

The model uses **MobileNetV2 transfer learning** with TensorFlow/Keras.

Training code is in:

```text
model/train.py
```

Prediction code is in:

```text
model/inference.py
```

After training, the model files are saved in:

```text
model/artifacts/
```

Generated files:

```text
food_cnn.keras
class_names.json
```

---

## 📊 Dataset Structure

Training images should be placed inside:

```text
model/dataset/
```

Folder structure:

```text
model/dataset/
│── banana/
│── bread/
│── burger/
│── chapati/
│── fried_rice/
│── grapes/
│── idli/
│── pizza/
│── salad/
│── samosa/
│── watermelon/
```

Each class should contain food images:

```text
model/dataset/samosa/samosa_001.jpg
model/dataset/samosa/samosa_002.jpg
```

Recommended dataset size:

```text
Minimum: 50 images per class
Better: 100-200 images per class
```

---

## 📥 Dataset Download

Download Indian food images:

```bash
python model/download_hf_indian_food.py
```

Download fruit/vegetable images:

```bash
python model/download_kaggle_fruits.py
```

---

## 🏋️ Train the Model

Run from the project root:

```bash
python model/train.py
```

The backend will use the CNN only after these files are created:

```text
model/artifacts/food_cnn.keras
model/artifacts/class_names.json
```

---

## 🧪 How to Run Locally

### 1. Run Backend

```bash
cd backend
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Backend runs at:

```text
http://127.0.0.1:8000
```

API docs:

```text
http://127.0.0.1:8000/docs
```

---

### 2. Run Frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

On Windows PowerShell, use:

```bash
npm.cmd run dev
```

Frontend runs at:

```text
http://localhost:3000
```

---

## 🔌 API Endpoint

### POST `/predict`

Form data:

```text
image      food image file
height_cm  user height in centimeters
weight_kg  user weight in kilograms
```

Example response:

```json
{
  "food": "samosa",
  "serving": "1 samosa",
  "calories": 262,
  "confidence": 0.91,
  "model_type": "cnn",
  "bmi": 22.0,
  "bmi_category": "Normal",
  "recommendation": "Your BMI is 22.0, which is normal...",
  "action_items": [
    "Add protein and fiber to balance the plate.",
    "Avoid extra sauces, sugar, and fried sides."
  ]
}
```

---

## ⚠️ Note

This project uses image classification, so it predicts one main food item per image.

If a plate contains multiple food items, the model may predict only the most dominant food item. For detecting multiple food items on one plate, an object detection model such as YOLO would be required.

Dataset images and trained model files are not uploaded to GitHub because they can be large.

---

## 📌 Future Improvements

* Add more food classes
* Add multi-food plate detection using object detection
* Add portion size estimation
* Add meal history tracking
* Add user login system
* Improve model accuracy with larger dataset
* Add nutrition details like protein, carbs, and fats

---

## 👩‍💻 Author

**Jahnavi Srivastava**

---
```
