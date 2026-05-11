def calculate_bmi(height_cm: float, weight_kg: float) -> float:
    if height_cm <= 0 or weight_kg <= 0:
        raise ValueError("Height and weight must be positive values.")

    height_m = height_cm / 100
    return round(weight_kg / (height_m * height_m), 1)


def bmi_category(bmi: float) -> str:
    if bmi < 18.5:
        return "Underweight"
    if bmi < 25:
        return "Normal"
    if bmi < 30:
        return "Overweight"
    return "Obese"


FRUIT_FOODS = {"apple", "banana", "grapes", "watermelon", "fruit_plate", "salad"}
FRIED_OR_DENSE_FOODS = {"samosa", "burger", "pizza", "fried_rice", "bread"}


def calorie_recommendation(
    bmi: float,
    detected_calories: int,
    food_name: str,
    confidence: float,
) -> dict:
    category = bmi_category(bmi)
    readable_food = food_name.replace("_", " ")

    if food_name == "unknown_food" or confidence < 0.50:
        return {
            "summary": (
                "I cannot confidently identify this food from the image. Do not make a diet decision from this scan; "
                "retake the photo with one food item in clear light, or avoid eating it if you are unsure what it contains."
            ),
            "action_items": [
                "Retake the photo from the top with the plate fully visible.",
                "Separate mixed items so the scanner can identify each food.",
                "If it is oily, packaged, or unclear, skip it and choose a known whole-food option.",
            ],
        }

    action_items = []
    if category in {"Overweight", "Obese"}:
        if food_name in FRIED_OR_DENSE_FOODS:
            action_items.extend(
                [
                    f"Remove or reduce {readable_food}; it is calorie dense for your current BMI goal.",
                    "Add salad, curd, sprouts, or lean protein so the meal is more filling.",
                    "Keep the portion to half and avoid sugary drinks with it.",
                ]
            )
        elif food_name in FRUIT_FOODS:
            action_items.extend(
                [
                    "Good choice for a light meal, but keep fruit to one bowl.",
                    "Add protein like curd, paneer, eggs, or sprouts so you stay full longer.",
                    "Avoid adding sugar, cream, fruit juice, or extra fried snacks with this plate.",
                ]
            )
        else:
            action_items.extend(
                [
                    "Keep the portion controlled and stop at 80 percent full.",
                    "Remove fried sides, sauces, and extra oil from the plate.",
                    "Add vegetables and protein to improve satiety.",
                ]
            )
    elif category == "Underweight":
        action_items.extend(
            [
                "Add a protein source with this meal.",
                "Include healthy fats like nuts, peanut butter, or paneer if it fits your diet.",
                "Do not skip meals; build a steady calorie surplus.",
            ]
        )
    else:
        action_items.extend(
            [
                "This can fit your day if the portion matches your activity level.",
                "Add protein and fiber to balance the plate.",
                "Avoid extra sauces, sugar, and fried sides.",
            ]
        )

    if category == "Underweight":
        summary = (
            f"Your BMI is {bmi}, which is underweight. This meal is about "
            f"{detected_calories} kcal. Treat it as a base and build it up with protein and healthy fats."
        )
    elif category == "Normal":
        summary = (
            f"Your BMI is {bmi}, which is normal. This meal is about "
            f"{detected_calories} kcal. Keep the plate balanced and avoid unnecessary add-ons."
        )
    elif category == "Overweight":
        summary = (
            f"Your BMI is {bmi}, which is overweight. This meal is about "
            f"{detected_calories} kcal. For fat loss, prioritize portion control, protein, and fiber."
        )
    else:
        summary = (
            f"Your BMI is {bmi}, which is obese. This meal is about "
            f"{detected_calories} kcal. Choose lighter portions and get a professional plan if possible."
        )

    return {"summary": summary, "action_items": action_items}
