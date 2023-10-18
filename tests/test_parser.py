import pytest
from recipeservice.api.parser import parse_madplannu
from recipeservice.database.schema import BaseRecipe, Energy, Ingredient

raw_recipe =   {
    "id": 103,
    "title": "Recipe",
    "approach": "this is an approach",
    "categories": [
      {
        "mealcatid": 0,
        "mealcatname": "MealCategory1"
      },
      {
        "mealcatid": 1,
        "mealcatname": "MealCategory2"
      },
    ],
    "backlink": "https://www.website.com/recipe/103",
    "servingstotal": 2,
    "servingtype": "pers.",
    "energy": {
      "isavailable": True,
      "kcal": 298.0,
      "kj": 1247.0,
      "fat": 31.0565,
      "proteine": 16.3549,
      "dietary": 1.3123,
      "carbonhydrate": 51.2763,
      "fatrounded": 31.0,
      "proteinerounded": 16.0,
      "dietaryrounded": 1.0,
      "energy100g": "148 Kcal/100 g",
      "carbonhydraterounded": 51.0
    },
    "ingredients": [
      {
        "amount": 0.25,
        "unit": "stk.",
        "item": "Beans",
        "section": None,
        "foodid": 5
      },
      {
        "amount": 500.0,
        "unit": "g",
        "item": "Tomato",
        "section": None,
        "foodid": 1
      },
    ],
  }

ex_recipe = BaseRecipe(
    title="Recipe", servings=2, instructions="this is an approach", url="https://www.website.com/recipe/103", 
    energy=Energy(calories=298.0, fat=31.0565, protein=16.3549,carbohydrates=51.2763), ingredients=[
        Ingredient(amount=0.25, unit="stk.", item="Beans"),
        Ingredient(amount=500.0, unit="g", item="Tomato"),
    ],
    tags=["MealCategory1", "MealCategory2"]
)

def test_mealplannu_parser(): 
    recipe = parse_madplannu(raw_recipe)
    assert recipe.model_dump() == ex_recipe.model_dump()