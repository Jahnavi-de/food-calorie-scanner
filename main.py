from io import BytesIO

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image, UnidentifiedImageError

from app.ml.predictor import FoodPredictor
from app.ml.recommendation import (
    bmi_category,
    calculate_bmi,
    calorie_recommendation,
)

app = FastAPI(title="Food Calorie Scanner API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

predictor = FoodPredictor()


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "model_ready": predictor.model_ready}


@app.post("/predict")
async def predict_food(
    image: UploadFile = File(...),
    height_cm: float = Form(...),
    weight_kg: float = Form(...),
) -> dict:
    if not image.content_type or not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Please upload a valid image file.")

    try:
        payload = await image.read()
        pil_image = Image.open(BytesIO(payload))
        prediction = predictor.predict(pil_image)
        bmi = calculate_bmi(height_cm=height_cm, weight_kg=weight_kg)
    except UnidentifiedImageError as exc:
        raise HTTPException(status_code=400, detail="Could not read the uploaded image.") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    trainer_note = calorie_recommendation(
        bmi=bmi,
        detected_calories=prediction["calories"],
        food_name=prediction["food"],
        confidence=prediction["confidence"],
    )

    return {
        **prediction,
        "bmi": bmi,
        "bmi_category": bmi_category(bmi),
        "recommendation": trainer_note["summary"],
        "action_items": trainer_note["action_items"],
    }
