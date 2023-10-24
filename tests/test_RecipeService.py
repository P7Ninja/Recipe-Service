
import pytest
import shutil
import json
from pytest import FixtureRequest
from pathlib import Path
from fastapi import FastAPI
from fastapi.testclient import TestClient
from recipeservice import RecipeService, SQLRecipeDB


@pytest.fixture
def client(request: FixtureRequest, tmp_path: Path):
    db_path = tmp_path / "db"
    db_path.mkdir()
    db_file = db_path / "db.sql"
    shutil.copyfile("./tests/test.db", db_file)

    db = SQLRecipeDB({"DB_CONN": f"sqlite:///{db_file}"})
    app = FastAPI()
    service = RecipeService(app, db, dict())
    db.startup()
    service.configure_routes()
    request.addfinalizer(lambda: db.shutdown())

    return TestClient(app)

def test_random_recipe(client: TestClient):
    res = client.get("/recipe/random")
    assert res.status_code == 200

    recipe = res.json()

    assert isinstance(recipe, dict)

    assert list(recipe.keys()) == ["title", "servings", "instructions", "url", "energy", "ingredients", "tags", "id"]

def test_get_recipe(client: TestClient):
    expected = {'title': 'Aftensmad4', 'servings': 2, 'instructions': 'Aftensmad4', 'url': 'https://recipe.com/recipe/4', 'energy': {'calories': 210.24, 'fat': 21.67, 'protein': 37.19, 'carbohydrates': 25.27}, 'ingredients': [{'amount': 456.41, 'unit': 'g', 'item': 'tomat'}, {'amount': 19.2, 'unit': 'ml', 'item': 'mælk'}, {'amount': 347.11, 'unit': 'g', 'item': 'bønner'}], 'tags': ['Aftensmad'], 'id': 5}
    res = client.get("/recipe/5")
    assert res.status_code == 200

    recipe = res.json()
    assert recipe == expected


def test_get_recipes(client: TestClient):
    res = client.get("/recipe")
    assert res.status_code == 200

    recipes =  res.json()

    assert isinstance(recipes, list)
    assert len(recipes) == 25



def test_default(client: TestClient):
    res = client.get("/")
    assert res.status_code == 200

    assert res.json() == {"message": "Recipe-Service"}