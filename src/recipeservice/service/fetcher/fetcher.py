from urllib.parse import urlsplit
from bs4 import BeautifulSoup, Tag
import requests

def fetch_valdemar_recipe(url: str):
    if urlsplit(url).netloc != "www.valdemarsro.dk":
        raise Exception(f"{url} is not valdemarsro")
    
    res = requests.get(url)
    dom = BeautifulSoup(res.text, features="html.parser")
    name = dom.find("h2", attrs={"itemprop":"name"}).text
    stats = []
    stat: Tag
    for stat in dom.find_all("div", attrs={"class":"recipe-stat"}):
        key = stat.find("span", attrs={"class": "recipe-stat-label"}).text
        value = stat.find("strong").text
        stats.append({"name": key, "value": value})

    image = dom.find("div", attrs={"class":"recipe-image"}).find("img").attrs["src"]
    ingredients = []

    for ing in dom.find_all("li", attrs={"itemprop":"recipeIngredient"}):
        ingredients.append(ing.text)

    instructions = []
    for ins in dom.find_all("div", attrs={"itemprop": "recipeInstructions"}):
        instructions.append(ins.text)

    tags = []
    tag: Tag
    for tag in dom.find("div", attrs={"class": "recipe-bar"}).children:
        text = tag.text.strip().replace("\n", "")
        if text == "":
            continue
        tags.append(text)
    return {
        "name": name,
        "stats": stats,
        "ingredients": ingredients,
        "instructions": instructions,
        "url": url,
        "image": image,
        "tags": tags
    }