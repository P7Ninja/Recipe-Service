from ..database.datastructure import *

def parse_valdemar_recipe(recipe: dict, units: set):
    tags = {t.lower() for t in recipe["tags"]}
    if not any(x in t for x in ["aftensmad", "morgenmad", "frokost", "snacks"] for t in tags):
        return None
    title = recipe["name"]
    portions, isMeal = parsePortion(recipe["stats"])
    ins = recipe["instructions"][0]
    ings = []
    for i in recipe["ingredients"]:
        ing = parseIngredient(i, units) 
        if ing is None:
            continue
        ings.append(ing)
    return BaseRecipe(
        title=title, 
        portionSize=float(portions), 
        isMeal=isMeal, 
        instructions=ins, 
        ingredients=ings, 
        url=recipe["url"], 
        tags=recipe["tags"]
        )
    

def parsePortion(stats: list[dict]):
    value: str = next((s for s in stats if "Antal" in s["name"]), dict).get("value", "")
    return value.split(" ")[0], "pers." in value

def parseIngredient(ingredientStr: str, units: set):
    parts = ingredientStr.split(" ")
    if "," in parts[0] and parts[0].replace(",", "").isdigit():
        ingredientStr = parts[0].replace(",", ".") + " " + " ".join(parts[1:])
    if "," not in ingredientStr:
        return parseNoInstructionIngredient(ingredientStr, units)
    else:
        return parseInstructionIngredient(ingredientStr, units)

def parseNoInstructionIngredient(ingredientStr: str, units: set):
    parts = ingredientStr.split(" ")
    partsLen = len(parts)
    isNumber = parts[0].replace(".", "").isdigit()
    if partsLen == 1:
        return Ingredient(item=parts[0])
    if partsLen == 2 and isNumber:
        return Ingredient(amount=float(parts[0]), item=parts[1])
    if partsLen == 2:
        return Ingredient(item=ingredientStr)
    if partsLen >= 3 and isNumber:
        if parts[1] in units:
            return Ingredient(amount=float(parts[0]), unit=parts[1], instructions=" ".join(parts[2:]))
        return Ingredient(amount=float(parts[0]), item=" ".join(parts[1:]))
    return None

def parseInstructionIngredient(ingredientStr: str, units: set):
    parts = ingredientStr.split(" ")
    index = parts.index(next((i for i in parts if "," in i), None)) + 1
    noInstruction = " ".join(parts[:index])[:-1]
    ingredient =  parseNoInstructionIngredient(noInstruction, units)
    if ingredient is not None:
        ingredient.instructions = " ".join(parts[index:])
    return ingredient
