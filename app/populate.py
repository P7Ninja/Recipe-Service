from tqdm import tqdm
from argparse import ArgumentParser
import json
import os

from recipeservice.api.parser import parse_madplannu
from recipeservice.database import SQLRecipeDB

if __name__ == "__main__":
    parser = ArgumentParser(description="Populate SQL Database from Mad plan nu recipes")
    parser.add_argument("file", help="File to parse")
    parser.add_argument("connection", help="Connection string to SQL database (sqlalchemy string)")
    args = parser.parse_args()

    db = SQLRecipeDB({"DB_CONN": args.connection})
    db.startup()
    parse_error, create_error = 0, 0
    with open(args.file, "r", encoding="utf-8") as f:
        recipes: list[dict] = json.load(f)

        # remove duplicates
        ids = set()
        unique = []
        for r in recipes:
            if r["id"] in ids:
               continue
            unique.append(r)
            ids.add(r["id"])

        url = set()
        for recipe in tqdm(unique):
            if recipe["backlink"] in url:
                continue
            url.add(recipe["backlink"])
            parsed = parse_madplannu(recipe)
            if parsed is None:
                parse_error += 1
                continue
            if db.create_recipe(parsed) == -1:
                create_error += 1
        print(f"Finished with {parse_error} parse skipped and {create_error} create errors")

    db.shutdown()