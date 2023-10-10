import json
import re
from ..database.datastructure import *


# with open('recipes_raw.json', encoding="utf8") as fp:
#     recipes = json.loads(fp.read())
#     fp.close()


def parse_MealDB_recipe(recipe)->Recipe:
    url = 'www.themealdb.com/api/json/v1/1/lookup.php?i=' + recipe['idMeal']
    title = recipe['name']
    instructions = recipe['instructions']
    
    
    strTags : str = recipe['strTags'] # strTags
    if strTags != None:
        tags : list[str] = strTags.split(",")
    else:
        tags = ""
    
    ingredients = get_ingredients(recipe)
        
    r = Recipe(title=title, portionSize=1, isMeal=True, instructions=instructions, ingredients=ingredients, url=url, tags=tags)
    return r

def get_ingredients(recipe):
    ingredients = []
    for i in range(1, 20):
        ingredient_name = recipe['strIngredient' + str(i)]
        p = r'([0-9]*)[ ]*([a-zA-Z0-9 ]*[ ]*[ a-zA-Z]*)'
        match = None
        
        if ingredient_name != None and ingredient_name != '':
            match = re.match(p, recipe['strMeasure' + str(i)])
        if match:
            measure = match.groups()    
            ingredients[i] = Ingredient(amount=measure[0], unit=measure[1], item=ingredient_name, instructions="")
    return ingredients

    
    

