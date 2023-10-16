from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

from .BaseRecipeDB import BaseRecipeDB
from .model import sql as model
from . import schema
from .factory import recipe_from_schema, recipe_from_sql_model

class SQLRecipeDB(BaseRecipeDB):
        def __init__(self, cfg: dict) -> None:
            super().__init__(cfg)
                
        def startup(self, connect_args: dict=dict()):
            self.__engine = create_engine(self.cfg["DB_CONN"], connect_args=connect_args)
            self.__local = sessionmaker(autocommit=False, autoflush=False, bind=self.__engine)
            self.__db = self.__local()
            model.Base.metadata.create_all(self.__engine)

        def shutdown(self):
            self.__local.close_all()
            self.__engine.dispose()
        
        def get_recipes(self):
            return self.__db.query(model.Recipe).limit(100).all()
        
        def create_recipe(self, recipe: schema.BaseRecipe):
            db_recipe = recipe_from_schema(self.__db, recipe)
            return db_recipe.id

        def get_recipe(self, id: int):
            return self.__db.query(model.Recipe).filter(model.Recipe.id == id).first()
        
        def get_random_recipe(self, calories: float=.0, protein: float=.0, fat: float=.0, carbs: float=.0, energy_error: float=.0, tags: list[str]=None):
            calMin, calMax = minMax(calories, energy_error)
            proMin, proMax = minMax(protein, energy_error)
            fatMin, fatMax = minMax(fat, energy_error)
            carbMin, carbMax = minMax(carbs, energy_error)
            recipes = self.__db.query(model.Recipe)\
                .join(model.Energy)\
                .filter(
                    model.Energy.calories <= calMax,
                    model.Energy.calories >= calMin,
                    model.Energy.protein <= proMax,
                    model.Energy.protein >= proMin,
                    model.Energy.fat >= fatMin,
                    model.Energy.fat <= fatMax,
                    model.Energy.carbohydrates <= carbMax,
                    model.Energy.carbohydrates >= carbMin,
                    )
            if tags is not None:
                recipes = recipes.join(model.recipe_tag_association).join(model.Tag)\
                    .filter(model.Tag.tag.in_(tags))
            recipe = recipes.order_by(func.random()).first()
            if recipe is None:
                return None
            return recipe_from_sql_model(recipe)
        
        def delete_recipe(self, id: int):
            try:
                recipe = self.get_recipe(id)
                if recipe is None:
                    return False
                self.__db.delete(recipe)
                self.__db.commit()
            except:
                return False
            return True


def minMax(num: float, error: float):
    if num == 0:
        return 0, 999999
    numError = (num * error)
    return num - numError,  num + numError