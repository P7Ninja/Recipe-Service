from . import schema

class BaseRecipeDB:
        def __init__(self, cfg: dict) -> None:
            self.cfg = cfg
                
        def startup(self):
            return
        
        def shutdown(self):
            return
        
        def create(self):
            return
        
        def get_recipes(self) -> list[schema.Recipe]:
            return
        
        def create_recipe(self, recipe: schema.BaseRecipe) -> schema.Recipe:
            return
        
        def get_recipe(self, id: int) -> schema.Recipe:
            return
    
        def update_recipe(self, id: int, recipe: schema.BaseRecipe) -> schema.Recipe:
            raise NotImplementedError("Not Implemented!")
        
        def delete_recipe(self, id: int) -> schema.Recipe:
            return