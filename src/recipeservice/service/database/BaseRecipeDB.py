from .datastructure import BaseRecipe, Recipe

class BaseRecipeDB:
        def __init__(self, cfg: dict) -> None:
            self.cfg = cfg
                
        def __contains__(self, url):
            return False
        
        def __getitem__(self, url):
            return BaseRecipe()
                
        def startup(self):
            return
        
        def shutdown(self):
            return
        
        def get_recipes(self, tags: list[str] = [], ingredients: list[str] = [], serving: int=1, i: int=100, name: str="") -> list[Recipe]:
            return
        
        def create_recipe(self, recipe: BaseRecipe) -> Recipe:
            return
        
        def get_recipe(self, id: int=-1, serving: int=1, url: str=None) -> Recipe:
            return
    
        def update_recipe(self, id: int, recipe: BaseRecipe) -> Recipe:
            return
        
        def delete_recipe(self, id: int) -> Recipe:
            return