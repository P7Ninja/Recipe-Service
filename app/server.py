from fastapi import FastAPI
from recipeservice import RecipeService, SQLRecipeDB
import os

cfg = os.environ

app = FastAPI()
db = SQLRecipeDB(cfg)
service = RecipeService(app, db, cfg)

service.configure_database()
service.configure_routes()