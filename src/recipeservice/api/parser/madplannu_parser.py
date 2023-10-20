from ...database.schema import *

def parse_madplannu(recipe: dict):
    if recipe["servingtype"] != "pers.":
        return None
    title = recipe["title"]
    servings = recipe["servingstotal"]
    instructions = recipe["approach"]
    url = recipe["backlink"]
    raw_energy = recipe["energy"]
    energy = Energy(
        calories = raw_energy["kcal"],
        fat = raw_energy["fat"],
        protein= raw_energy["proteine"],
        carbohydrates= raw_energy["carbonhydrate"]
    )
    ingredients = []
    for i in recipe["ingredients"]:
        if any(i[arg] is None for arg in ["amount", "unit", "item"]):
            return None
        ingredients.append(Ingredient(
            amount=i["amount"],
            unit=i["unit"],
            item=i["item"]
        ))

    tags = []
    for t in recipe["categories"]:
        tags.append(t["mealcatname"])
    return BaseRecipe(
        title=title,
        servings=servings,
        instructions=instructions,
        ingredients=ingredients,
        energy=energy,
        tags=tags,
        url=url
    )