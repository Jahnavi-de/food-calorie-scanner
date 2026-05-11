CALORIE_TABLE = {
    "banana": {"serving": "1 medium banana", "calories": 105},
    "bread": {"serving": "1 bread piece", "calories": 140},
    "burger": {"serving": "1 regular burger", "calories": 295},
    "chapati": {"serving": "1 medium chapati", "calories": 120},
    "fried_rice": {"serving": "1 plate fried rice", "calories": 333},
    "fruit_plate": {"serving": "1 mixed fruit plate", "calories": 150},
    "grapes": {"serving": "1 small bowl grapes", "calories": 104},
    "idli": {"serving": "2 idli", "calories": 116},
    "pizza": {"serving": "1 slice pizza", "calories": 285},
    "salad": {"serving": "1 bowl salad", "calories": 80},
    "samosa": {"serving": "1 samosa", "calories": 262},
    "watermelon": {"serving": "1 bowl watermelon", "calories": 46},
    "unknown_food": {"serving": "unclear serving", "calories": 0},
}


def food_details(food_name: str) -> dict:
    details = CALORIE_TABLE.get(food_name, {"serving": "1 serving", "calories": 200})
    return {"food": food_name, **details}

