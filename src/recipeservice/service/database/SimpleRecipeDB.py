from .BaseRecipeDB import BaseRecipeDB
from .datastructure import BaseRecipe, Recipe

class SimpleRecipeDB(BaseRecipeDB):
    def __init__(self, cfg: dict) -> None:
        super().__init__(cfg)
        self.__recipes: dict[int, Recipe] = dict()
            
    def __contains__(self, url):
        return any(url in r.url for r in self.__recipes.values())
    
    def __getitem__(self, url):
        for r in self.__recipes.values():
            if url in r:
                return r
        return None
    
            
    def startup(self):
        return
    
    def shutdown(self):
        return
    
    def get_recipes(self, tags: list[str] = [], ingredients: list[str] = [], serving: int=1, i: int=100, title: str="") -> list[Recipe]:
        recipe_filter = list(self.__recipes.values())

        if title != "":
            recipe_filter = filter(lambda r: title in r.title, recipe_filter)

        if len(ingredients) > 0:
            include = i/ 100
            recipe_filter = filter(lambda r: ingredient_filter(ingredients, r, include), recipe_filter)
        if len(tags) > 0:
            recipe_filter = filter(lambda r: any(t.lower() in [rt.lower() for rt in r.tags] for t in tags), recipe_filter)
        return list(recipe_filter)
    
    def create_recipe(self, recipe: BaseRecipe) -> Recipe:
            keys = list(self.__recipes.keys())
            index = max(keys if keys != [] else [-1]) + 1
            self.__recipes[index] = Recipe(**recipe.model_dump(), id=index)
            return self.__recipes[index]
    
    def get_recipe(self, id: int=-1, serving: int=1, url: str=None) -> Recipe:
        if url is not None:
            return self.__getitem__(url)
        return self.__recipes[id]
        
    def update_recipe(self, id: int, recipe: BaseRecipe) -> Recipe:
        self.__recipes[id] = recipe
        return recipe
    
    def delete_recipe(self, id: int) -> Recipe:
        recipe = self.__recipes[id]
        del self.__recipes[id]
        return recipe
        
def ingredient_filter(search_items: list[str], recipe: BaseRecipe, include: float):
    ingredients = 0
    for item in search_items:
        for ingredient in recipe.ingredients:
            ritem = ingredient.item
            if item.lower() in ritem.lower():
                ingredients += 1

    percentage = ingredients / len(recipe.ingredients)
    return percentage >= include