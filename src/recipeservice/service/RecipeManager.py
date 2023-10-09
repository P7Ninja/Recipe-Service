
from typing import Callable
from urllib.parse import urlsplit, parse_qs

from .database.datastructure import *
from .database.BaseRecipeDB import BaseRecipeDB

class BaseRecipeManager:
    def fetch(self, url: str):pass
    def parse(self, recipe_dict: dict, source: str):pass
    def query(self, query: str):pass
    def add_domain(self, domain: str, fetcher: Callable, parser: Callable):pass

class RecipeManager(BaseRecipeManager):
    def __init__(self, db: BaseRecipeDB) -> None:
        self.db = db
        self.units: set = set()
    
        self.__fetcher: dict[str, Callable] = dict()
        self.__parser:  dict[str, Callable] = dict()
    
    def fetch(self, url: str):
        recipe = self.db.get_recipe(url=url)
        if recipe is not None:
            return recipe
        
        key = urlsplit(url).netloc
        if key not in self.__fetcher:
            raise Exception(f"No Fetcher for {key}!")
        
        res = self.__fetcher[key](url)
        recipe = self.parse(res, key)
        return recipe

    def parse(self, recipe_dict: dict, source: str) -> Recipe | None:
        if source not in self.__parser:
            raise Exception(f"No Parser for {source}!")
        
        parser = self.__parser[source]
        recipe: BaseRecipe = parser(recipe_dict, self.units)

        if recipe is None:
            return None
        
        return self.db.create_recipe(recipe)
    
    def add_domain(self, domain: str, fetcher: Callable, parser: Callable):
        self.__fetcher[domain] = fetcher
        self.__parser[domain] = parser

