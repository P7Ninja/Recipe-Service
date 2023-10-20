import json
import re
from ...database.schema import *

def parse_MealDB_recipe(recipes):
    recipe = recipes['meals'][0]
    
    id = recipe['idMeal']
    url = 'https://www.themealdb.com/api/json/v1/1/lookup.php?i=' + id
    title = recipe['strMeal']
    instructions = recipe['strInstructions']
    
    
    strTags : str = recipe['strTags'] # strTags
    if strTags != None:
        tags : list[str] = strTags.split(",")
    else:
        tags = ""
    
    ingredients : list[Ingredient] = get_ingredients(recipe)
        
    r = Recipe(title=str(title), portionSize=1, isMeal=True, instructions=instructions, ingredients=ingredients, url=str(url), tags=tags, id=id)
    return r

def get_ingredients(recipe):
    ingredients = []
    for i in range(1, 20):
        ingredient_name = recipe['strIngredient' + str(i)]
        p = r'([0-9]*)[ ]*([a-zA-Z0-9 ]*[ ]*[ a-zA-Z]*)'
        match = None
        
        if ingredient_name != None and ingredient_name != '':
            match = re.match(p, recipe['strMeasure' + str(i)])
        if match != None:
            measure = match.groups()
            if measure[0] == '':
                measure = (1, measure[1])
            ing = Ingredient(amount=measure[0], unit=str(measure[1]), item=str(ingredient_name), instructions="")
            ingredients.append(ing)
    return ingredients


    
    

