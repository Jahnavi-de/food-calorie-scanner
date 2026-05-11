# Food Calorie Scanner

Food Calorie Scanner is a full-stack web application that detects food from an uploaded image, estimates calories, calculates BMI, and gives fitness-style recommendations.

The project uses a Next.js frontend, FastAPI backend, and a TensorFlow/Keras CNN model trained with MobileNetV2 transfer learning.

## Features

- Upload a food image from the browser
- Predict food class using a trained CNN model
- Estimate calories and serving size
- Calculate BMI using height and weight
- Show BMI category
- Give fitness-style food recommendations
- Return `unknown_food` when prediction confidence is low
- Show top 3 predictions for debugging
- FastAPI REST API integration with Next.js frontend

## Tech Stack

### Frontend
- Next.js
- React
- TypeScript
- CSS

### Backend
- Python
- FastAPI
- Uvicorn
- Pillow

### Machine Learning
- TensorFlow
- Keras
- MobileNetV2 transfer learning
- NumPy

## Food Classes

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
