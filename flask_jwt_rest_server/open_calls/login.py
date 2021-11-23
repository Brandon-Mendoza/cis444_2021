from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token

import jwt

from tools.logging import logger

def handle_request():
    logger.debug("Login Handle Request")
    #use data here to auth the user

    password_from_user_form = request.form['password']
    username_from_user_form = request.form['username']

    cursor = g.db.cursor()
    cursor.execute("select * from users where username = '%s';" % (username_from_user_form))

    db_row = cursor.fetchone()

    if db_row is None:
        return json_response(data={"message": "The username '" + username_from_user_form + "' does not exist."}, status=404)
    else:
        
        if password_from_user_form == db_row[2]:
            user = {"user_id": db_row[0]}
            return json_response(data={"jwt": create_token(user)})
        else:
            return json_response(data={"message": "The password for '" + username_from_user_form + "' is invalid."}, status=404)
