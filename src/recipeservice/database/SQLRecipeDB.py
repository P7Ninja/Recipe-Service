from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from .BaseRecipeDB import BaseRecipeDB
from .model import sql as model
from . import schema

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
            db_energy = model.Energy(
                calories      = recipe.energy.calories,
                fat           = recipe.energy.fat,
                protein       = recipe.energy.protein,
                carbohydrates = recipe.energy.carbohydrates,
            )

            db_recipe = model.Recipe(
                title        = recipe.title,
                servings     = recipe.servings,
                instructions = recipe.instructions,
                energy       = db_energy,
                url          = recipe.url
            )

            ingredients = []
            item_cache = dict()
            unit_cache = dict()
            for ingredient in recipe.ingredients:
                db_item = self.__db.query(model.Item).filter(model.Item.name == ingredient.item).first()
                if db_item is None:
                    db_item = item_cache.get(ingredient.item, None)
                if db_item is None:
                    db_item = model.Item(name=ingredient.item)
                    item_cache[ingredient.item] = db_item

                db_unit = self.__db.query(model.Unit).filter(model.Unit.name == ingredient.unit).first()
                if db_unit is None:
                    db_unit =unit_cache.get(ingredient.unit, None)
                if db_unit is None:
                    db_unit = model.Unit(name=ingredient.unit)
                    unit_cache[ingredient.unit] = db_unit

                db_ingredient = model.Ingredient(
                    amount = ingredient.amount,
                    unit   = db_unit,
                    item   = db_item
                )
                ingredients.append(db_ingredient)

            db_recipe.ingredients = ingredients

            tags = []
            tag_cache = dict()
            for tag in recipe.tags:
                db_tag = self.__db.query(model.Tag).filter(model.Tag.tag == tag).first()
                if db_tag is None:
                    db_tag = tag_cache.get(tag, None)
                if db_tag is None:
                    db_tag = model.Tag(tag=tag)
                    tag_cache[tag] = db_tag
                tags.append(db_tag)
            
            db_recipe.tags = tags

            self.__db.add(db_recipe)
            self.__db.commit()
            self.__db.refresh(db_recipe)

            return db_recipe.id

        def get_recipe(self, id: int):
            return self.__db.query(model.Recipe).filter(model.Recipe.id == id).first()
        
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
