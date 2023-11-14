import pytest
import shutil
from pytest import FixtureRequest
from pathlib import Path
from fastapi import HTTPException

from recipeservice import SQLRecipeDB
from recipeservice.database.schema import BaseRecipe, Ingredient, Energy

@pytest.fixture
def db(request: FixtureRequest, tmp_path: Path):
    db_path = tmp_path / "db"
    db_path.mkdir()
    db_file = db_path / "db.sql"
    shutil.copyfile("./tests/test.db", db_file)
    db = SQLRecipeDB({"DB_CONN": f"sqlite:///{db_file}"})
    db.startup()
    def tearddown():
        db.shutdown()

    request.addfinalizer(tearddown)
    return db

def test_db_get_recipes(db: SQLRecipeDB):
    assert len(db.get_recipes()) == 25



def test_db_create_recipe_success(db: SQLRecipeDB):
    new_recipe = BaseRecipe(
        title="test",
        servings=1,
        instructions="test ins",
        url="https://www.test.com/recipe/4342",
        energy=Energy(calories=500.0, fat=20.0, protein=30.0, carbohydrates=50.0),
        ingredients=[Ingredient(amount=500, unit="g", item="beans")],
        tags=["Aftensmad"]

    )
    id = db.create_recipe(new_recipe)
    db_recipe = db.get_recipe(id).model_dump()
    db_id = db_recipe["id"]
    del db_recipe["id"]
    assert db_recipe == new_recipe.model_dump()
    assert id == db_id
    
def test_db_create_recipe_no_recipe(db: SQLRecipeDB):
    try:
        db.create_recipe(None)
    except HTTPException as e:
        assert e.status_code == 400




def test_db_get_random_recipe(db: SQLRecipeDB):
    res = [
        ({"calories": 322.6}, 21),
        ({"fat": 43.5}, 4),
    ]

    for input, ex in res:
        id = db.get_random_recipe(**input).id
        assert id == ex

def test_db_get_random_recipe_no_recipe(db: SQLRecipeDB):
    try:
        db.get_random_recipe(calories=100000)
    except HTTPException as e:
        assert e.status_code == 500



def test_db_delete_recipe_success(db: SQLRecipeDB):
    assert db.delete_recipe(4) == True

def test_db_delete_recipe_no_id(db: SQLRecipeDB):
    try:
        db.delete_recipe(None)
    except HTTPException as e:
        assert e.status_code == 400

def test_db_delete_recipe_no_recipe(db: SQLRecipeDB):
    try:
        db.delete_recipe(50)
    except HTTPException as e:
        assert e.status_code == 404

def test_db_delete_recipe_fail(db: SQLRecipeDB):
    try:
        db.delete_recipe(4)
    except HTTPException as e:
        assert e.status_code == 500
        