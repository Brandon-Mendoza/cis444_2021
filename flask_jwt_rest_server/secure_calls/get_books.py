from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token

import json

from tools.logging import logger

def handle_request():
    logger.debug("Get Books Handle Request")

    cursor = g.db.cursor()

    try:
        user_id = g.jwt_data['user_id']

        #select * from books;
        cursor.execute("select * from books;", user_id)
        print("Books retrieved")
        
    except:
         print("books unable to be found")
         return json_response(data={"message": "books unable to be found."}, status=500)

     
    message = "{\"books\":["
    bookCounter = 0
                 
    while True:
        db_row = cursor.fetchone()
                                 

        if db_row is None:
            print("No more books to add.")
            break;
        else:
            print("Adding Book...")
                                                                                 
            if bookCounter > 0: message += ","
                                                                                 

            bookCounter += 1
                                                                                                 

            message += "{\"author\": \"%s\", \"title\": \"%s\", \"price\": %s, \"book_id\": %s}" % (db_row[1], db_row[2], str(db_row[3]), str(db_row[0]))
            print("Book added.")
                                                                                                                                             
    message += "]}"
    print("The books were created.")
    return json_response(data=json.loads(message))
