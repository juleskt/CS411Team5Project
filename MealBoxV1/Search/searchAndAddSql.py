from django.db import connection, connections
import json

def searchDBCacheForSearch(searchTerm):
    cursor = connection.cursor()
    cursor.execute("""
        SELECT
            *
        FROM
            searchCache_tbl
        WHERE
            search_term = %s
        """, [searchTerm])

    return cursor.fetchone()


def insertSearchIntoDBCache(searchTerm, jsonResult):
    cursor = connection.cursor()
    result = cursor.execute("""
        INSERT INTO
            searchCache_tbl
            (
                search_term,
                data_response,
                page_num,
                date_cached
            )
            VALUES
            (
                %s,
                %s,
                %s,
                CURDATE()
            )

        """, [searchTerm, json.dumps(jsonResult), 1])

    print("INSERT RESULT: ", result)


def updateSearchIntoDBCache(searchTerm, jsonResult):
    cursor = connection.cursor()
    result = cursor.execute("""
        UPDATE
            searchCache_tbl
        SET
            data_response = %s,
            page_num = %s,
            date_cached = CURDATE()
        WHERE
          search_term = %s
        """, [json.dumps(jsonResult), 1, searchTerm])

    print("INSERT RESULT: ", result)


def updateDataAndDateDBCache(searchTerm, jsonResult):
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE
            searchCache_tbl
        SET
            data_response=%s,
            date_cached=CURDATE()
        WHERE
            search_term = %s
        """, [jsonResult, searchTerm])


def addRecipeToDB(recipeID, recipeName, recipeURL, recipeImgURL):
    cursor = connections['users'].cursor()
    result = cursor.execute("""
        INSERT INTO
            Recipes_tbl
            (
                recipe_id,
                recipe_title,
                recipe_url,
                recipe_source
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s
            )
        """, [recipeID, recipeName, recipeImgURL, recipeURL])

    print("INSERT RESULT: ", result)


def searchDBForRecipe(recipeID):
    cursor = connections['users'].cursor()
    cursor.execute("""
        SELECT
            *
        FROM
            Recipes_tbl
        WHERE
            recipe_id = %s
        """, [recipeID])

    # https://docs.djangoproject.com/en/1.10/topics/db/sql/
    # Takes sql output and returns dictionary
    columns = [col[0] for col in cursor.description]

    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def searchDBForSavedRecipe(recipeID, userID):
    cursor = connections['users'].cursor()
    cursor.execute("""
        SELECT
            *
        FROM
            Saved_recipe_tbl
        WHERE
            recipe_id = %s AND
            user_id = %s
        """, [recipeID, userID])

    # https://docs.djangoproject.com/en/1.10/topics/db/sql/
    # Takes sql output and returns dictionary
    columns = [col[0] for col in cursor.description]

    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def addSavedRecipeForUser(recipeID, userID):
    cursor = connections['users'].cursor()
    result = cursor.execute("""
        INSERT INTO
            Saved_recipe_tbl
            (
                recipe_id,
                user_id
            )
            VALUES
            (
                %s,
                %s
            )
        """, [recipeID, userID])


def searchDBForSavedIngredient(ingredientName):
    print("INCOMING INGREDIENT:", ingredientName)
    cursor = connections['users'].cursor()
    cursor.execute("""
        SELECT
            *
        FROM
            Ingredient_tbl
        WHERE
            ingredient_name = %s
        """, [ingredientName])

    # https://docs.djangoproject.com/en/1.10/topics/db/sql/
    # Takes sql output and returns dictionary
    columns = [col[0] for col in cursor.description]

    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def addIngredientToDB(ingredientName):
    cursor = connections['users'].cursor()
    result = cursor.execute("""
        INSERT INTO
            Ingredient_tbl
            (
                ingredient_name
            )
            VALUES
            (
                %s
            )
        """, [ingredientName])

    print("INSERT RESULT: ", result)


def addIngredientToRecipe(recipeID, ingredientID, rawDescription):
    cursor = connections['users'].cursor()
    result = cursor.execute("""
        INSERT INTO
            Recipe_ingredient_tbl
            (
                recipe_id,
                ingredient_id,
                description
            )
            VALUES
            (
                %s,
                %s,
                %s
            )
        """, [recipeID, ingredientID, rawDescription])

    print("INSERT RESULT: ", result)


def deleteSavedRecipeFromDB(recipeID,userID):
    cursor = connections['users'].cursor()
    result = cursor.execute("""
            DELETE FROM
                Saved_recipe_tbl
            WHERE
                recipe_id = %s AND user_id = %s
            """, [recipeID, userID])


def getIngredientsFromRecipeID(recipeID):
    cursor = connections['users'].cursor()
    result = cursor.execute("""
                SELECT
                    *
                FROM
                  Recipe_ingredient_tbl
                INNER JOIN
                  Ingredient_tbl 
                  ON
                    Recipe_ingredient_tbl.ingredient_id = Ingredient_tbl.ingredient_id
                INNER JOIN
                  Recipes_tbl
                  ON 
                  Recipes_tbl.recipe_id = Recipe_ingredient_tbl.recipe_id
                WHERE 
                  Recipe_ingredient_tbl.recipe_id = %s

                """, [recipeID])

    columns = [col[0] for col in cursor.description]

    return [dict(zip(columns, row)) for row in cursor.fetchall()]
