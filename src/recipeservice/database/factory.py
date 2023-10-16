from .model import sql as model
from .schema import BaseRecipe, Recipe, Ingredient, Energy
from sqlalchemy.orm import Session

def recipe_from_sql_model(recipe: model.Recipe):
    return Recipe(
                id=recipe.id,
                title = recipe.title,
                servings=recipe.servings,
                instructions=recipe.instructions,
                url=recipe.url,
                ingredients=[Ingredient(amount=i.amount, unit=i.unit.name, item=i.item.name) for i in recipe.ingredients],
                tags=[t.tag for t in recipe.tags],
                energy=Energy(
                    calories=recipe.energy.calories,
                    fat=recipe.energy.fat,
                    protein=recipe.energy.protein,
                    carbohydrates=recipe.energy.carbohydrates,
                )
            )

def recipe_from_schema(session: Session, recipe: BaseRecipe):
    db_energy = model.Energy(
                calories      = recipe.energy.calories,
                fat           = recipe.energy.fat,
                protein       = recipe.energy.protein,
                carbohydrates = recipe.energy.carbohydrates,
            )

    db_recipe = model.Recipe(
        title        = recipe.title,
        servings     = recipe.servings,
        instructions = recipe.instructions,
        energy       = db_energy,
        url          = recipe.url
    )

    ingredients = []
    item_cache = dict()
    unit_cache = dict()
    for ingredient in recipe.ingredients:
        db_item = session.query(model.Item).filter(model.Item.name == ingredient.item).first()
        if db_item is None:
            db_item = item_cache.get(ingredient.item, None)
        if db_item is None:
            db_item = model.Item(name=ingredient.item)
            item_cache[ingredient.item] = db_item

        db_unit = session.query(model.Unit).filter(model.Unit.name == ingredient.unit).first()
        if db_unit is None:
            db_unit =unit_cache.get(ingredient.unit, None)
        if db_unit is None:
            db_unit = model.Unit(name=ingredient.unit)
            unit_cache[ingredient.unit] = db_unit

        db_ingredient = model.Ingredient(
            amount = ingredient.amount,
            unit   = db_unit,
            item   = db_item
        )
        ingredients.append(db_ingredient)

    db_recipe.ingredients = ingredients

    tags = []
    tag_cache = dict()
    for tag in recipe.tags:
        db_tag = session.query(model.Tag).filter(model.Tag.tag == tag).first()
        if db_tag is None:
            db_tag = tag_cache.get(tag, None)
        if db_tag is None:
            db_tag = model.Tag(tag=tag)
            tag_cache[tag] = db_tag
        tags.append(db_tag)
    
    db_recipe.tags = tags

    session.add(db_recipe)
    session.commit()
    session.refresh(db_recipe)

    return db_recipe