from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token


import json


from tools.logging import logger


def handle_request():
    logger.debug("Purchase Book Handle Request")

    cursor = g.db.cursor()


    try:
        cursor.execute("insert into purchased_books (user_id, book_id) VALUES (%s, %s);" % (str(g.jwt_data['user_id']), str(request.form['book_id']))) 
        g.db.commit()
        print("Book purchase was successful.")
        return json_response(data={"message": "You bought a book!"})


    except:
        print("Unable to add purchased book.")
        return json_response(data={"message": "Unable to add/buy book"}, status=500)
