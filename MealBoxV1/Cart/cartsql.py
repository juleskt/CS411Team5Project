from django.db import connection, connections
import json

def addCartID(cartID,userID):
    cursor = connections['users'].cursor()
    result = cursor.execute ("""
      UPDATE Users_tbl
      SET amazon_cart_id = %s
      WHERE user_amazon_id = %s
""", (cartID,userID))

def searchDBForCartID(userID):
    cursor = connections['users'].cursor()
    cursor.execute("""
        SELECT
            amazon_cart_id
        FROM
            Users_tbl
        WHERE
            user_amazon_id = %s
        """, [userID])