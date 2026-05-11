FOOD_CLASSES = [
    "apple",
    "banana",
    "burger",
    "chapati",
    "dal",
    "dosa",
    "egg",
    "fried_rice",
    "idli",
    "pizza",
    "salad",
    "samosa",
    "watermelon",
    "grapes",
    "fruit_plate",
    "bread",
    "unknown_food",
]

CALORIE_TABLE = {
    "apple": {"serving": "1 medium apple", "calories": 95},
    "banana": {"serving": "1 medium banana", "calories": 105},
    "burger": {"serving": "1 regular burger", "calories": 295},
    "chapati": {"serving": "1 medium chapati", "calories": 120},
    "dal": {"serving": "1 bowl dal", "calories": 180},
    "dosa": {"serving": "1 plain dosa", "calories": 168},
    "egg": {"serving": "1 boiled egg", "calories": 78},
    "fried_rice": {"serving": "1 plate fried rice", "calories": 333},
    "idli": {"serving": "2 idli", "calories": 116},
    "pizza": {"serving": "1 slice pizza", "calories": 285},
    "salad": {"serving": "1 bowl salad", "calories": 80},
    "samosa": {"serving": "1 samosa", "calories": 262},
    "watermelon": {"serving": "1 bowl watermelon", "calories": 46},
    "grapes": {"serving": "1 small bowl grapes", "calories": 104},
    "fruit_plate": {"serving": "1 mixed fruit plate", "calories": 150},
    "bread": {"serving": "1 bread piece", "calories": 140},
    "unknown_food": {"serving": "unclear serving", "calories": 0},
}


def get_food_details(food_name: str) -> dict:
    details = CALORIE_TABLE.get(food_name, {"serving": "1 serving", "calories": 200})
    return {"food": food_name, **details}
