from fastapi import FastAPI, Query, Request
from dotenv import dotenv_values
from typing import Annotated

from .service.database.datastructure import BaseRecipe
from .service.RecipeManager import RecipeManager
from .service.database.BaseRecipeDB import BaseRecipeDB
from .service.database.SimpleRecipeDB import SimpleRecipeDB
from .service.domains import domains
import pickle
import os

QueryList = Annotated[list[str] | None, Query()]

config = dotenv_values(".env")

if not os.path.exists("db.pkl"):
    db = SimpleRecipeDB(config)
else:
    with open("db.pkl", "rb") as f:
        db: BaseRecipeDB = pickle.load(f)

manager = RecipeManager(db)

for domain, fetch, parse in domains:
    manager.add_domain(domain, fetch, parse)
    
app = FastAPI()


@app.on_event("startup")
def startup():
    manager.db.startup()

@app.on_event("shutdown")
def shutdown():
    manager.db.shutdown()

@app.get("/")
async def root():
    return {"message": "Recipe-Service"}

@app.get("/recipe")
async def get_recipes(tag: QueryList = [], ingredient: QueryList = [], serving: int=1, i: int=100, name: str=""):
    return manager.db.get_recipes(tag, ingredient, serving, i, name)

@app.post("/recipe")
async def create_recipe(recipe: BaseRecipe):
    return manager.db.create_recipe(recipe)

@app.get("/recipe/{id}")
async def get_recipe(id: int, serving: int=1):
    return manager.db.get_recipe(id, serving)


@app.put("/recipe/{id}")
async def put_recipe(id: int, recipe: BaseRecipe):
    return manager.db.update_recipe(id, recipe)


@app.delete("/recipe/{id}")
async def delete_recipe(id: int):
    return manager.db.delete_recipe(id)


