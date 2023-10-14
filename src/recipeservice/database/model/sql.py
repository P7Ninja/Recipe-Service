from sqlalchemy.orm import declarative_base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Double, Table
from sqlalchemy.orm import relationship, DeclarativeBase

Base: DeclarativeBase = declarative_base()


recipe_tag_association = Table(
    "recipe_tag_association", 
    Base.metadata,
    Column("recipe_id", Integer, ForeignKey("recipes.id")),
    Column("tag_id", Integer, ForeignKey("tags.id"))
)

class Recipe(Base):
    __tablename__ = "recipes"
    id           = Column(Integer, nullable=False, autoincrement=True, primary_key=True)

    title        = Column(String, nullable=False)
    servings     = Column(Integer, nullable=False)
    instructions = Column(String)
    url          = Column(String, unique=True)

    energy       = relationship("Energy", back_populates="recipe", uselist=False, cascade="all, delete-orphan")
    ingredients  = relationship("Ingredient", back_populates="recipe", cascade="all, delete-orphan")
    tags = relationship("Tag", secondary=recipe_tag_association, back_populates="recipes")

class Energy(Base):
    __tablename__ = "energy"
    id            = Column(Integer, nullable=False, autoincrement=True, primary_key=True)

    calories      = Column(Double, nullable=False)
    fat           = Column(Double, nullable=False)
    protein       = Column(Double, nullable=False)
    carbohydrates = Column(Double, nullable=False)
    recipe_id     = Column(Integer, ForeignKey("recipes.id"))
    
    recipe        = relationship("Recipe", back_populates="energy")


class Ingredient(Base):
    __tablename__ = "ingredients"
    id        = Column(Integer, nullable=False, autoincrement=True, primary_key=True)

    amount    = Column(Double, nullable=False)
    unit_id   = Column(Integer, ForeignKey("units.id"))
    item_id   = Column(Integer, ForeignKey("items.id"))
    recipe_id = Column(Integer, ForeignKey("recipes.id"))

    unit      = relationship("Unit", back_populates="ingredients")
    item      = relationship("Item", back_populates="ingredients")
    recipe    = relationship("Recipe", back_populates="ingredients")

class Item(Base):
    __tablename__ = "items"
    id   = Column(Integer, nullable=False, autoincrement=True, primary_key=True)

    name = Column(String, nullable=False, unique=True)

    ingredients = relationship("Ingredient", back_populates="item")

class Unit(Base):
    __tablename__ = "units"
    id   = Column(Integer, nullable=False, autoincrement=True, primary_key=True)

    name = Column(String, nullable=False, unique=True)

    ingredients = relationship("Ingredient", back_populates="unit")


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    tag = Column(String, nullable=False, unique=True)

    recipes = relationship("Recipe", secondary=recipe_tag_association, back_populates="tags")
