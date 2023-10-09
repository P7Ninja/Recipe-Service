from pydantic import BaseModel


class Ingredient(BaseModel):
    amount: float = 0
    unit: str = ""
    item: str = ""
    instructions: str = ""


class BaseRecipe(BaseModel):
    title: str = ""
    portionSize: float = 0
    isMeal: bool = False
    instructions: str = ""
    ingredients: list[Ingredient] = None
    url: str = ""
    tags: list[str] = None

class Recipe(BaseRecipe):
    id: int