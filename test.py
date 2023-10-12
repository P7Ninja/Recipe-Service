from recipeservice.service.parser import parse_MealDB_recipe
from recipeservice.service.fetcher import fetch_MealDB_recipe

print(parse_MealDB_recipe(fetch_MealDB_recipe('https://www.themealdb.com/api/json/v1/1/lookup.php?i=52874')))