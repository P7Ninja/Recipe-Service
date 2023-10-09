from .fetcher import fetch_valdemar_recipe
from .parser import parse_valdemar_recipe

domains = [
    ("www.valdemarsro.dk",fetch_valdemar_recipe, parse_valdemar_recipe)
]