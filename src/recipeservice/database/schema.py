from pydantic import BaseModel

class BaseRecipe(BaseModel):
    title: str
    servings: int
    instructions: str
    url: str
    energy: 'Energy'
    ingredients: list['Ingredient']
    tags: list[str]

class Recipe(BaseRecipe):
    id: int

class Energy(BaseModel):
    calories: float
    fat: float
    protein: float
    carbohydrates: float
    
class Ingredient(BaseModel):
    amount: float
    unit: str
    item: str