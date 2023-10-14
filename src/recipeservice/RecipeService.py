from fastapi import FastAPI
from .database import BaseRecipeDB

class RecipeService:
    def __init__(self, app: FastAPI, database: BaseRecipeDB, cfg: dict) -> None:
        self.__app = app
        self.__db = database
        self.__cfg = cfg
        
    def configure_database(self):
        @self.__app.on_event("startup")
        def startup():
            self.__db.startup()
        
        @self.__app.on_event("shutdown")
        def shutdown():
            self.__db.shutdown()

    def configure_routes(self):
        self.__app.add_api_route("/api/recipe/{id}", self.get_recipe, methods=["GET"])
        self.__app.add_api_route("/api/recipe", self.get_recipes, methods=["GET"])

    def get_recipe(self, id: int):
        return self.__db.get_recipe(id)
    
    def get_recipes(self):
        return self.__db.get_recipes()