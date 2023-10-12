from .fetcher import fetch_valdemar_recipe, fetch_MealDB_recipe
from .parser import parse_valdemar_recipe, parse_MealDB_recipe


domains = [
    ("www.valdemarsro.dk",fetch_valdemar_recipe, parse_valdemar_recipe),
    ("www.themealdb.com", fetch_MealDB_recipe, parse_MealDB_recipe)
]