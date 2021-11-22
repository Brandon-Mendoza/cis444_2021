from flask import Flask,render_template,request
from flask_json import FlaskJSON, JsonError, json_response, as_json

import jwt
import json

import datetime
import bcrypt


from db_con import get_db_instance, get_db

app = Flask(__name__)
FlaskJSON(app)

USER_PASSWORDS = { "cjardin": "strong password"}

IMGS_URL = {
            "DEV" : "/static",
            "INT" : "https://cis-444-fall-2021.s3.us-west-2.amazonaws.com/images",
            "PRD" : "http://d2cbuxq67vowa3.cloudfront.net/images"
            }

CUR_ENV = "PRD"
JWT_SECRET = None
TOKEN = None

global_db_con = get_db()


with open("secret", "r") as f:
    JWT_SECRET = f.read()

#@app.route('/') #endpoint
#def index():
 #   return 'Web App with Python Caprice!' + USER_PASSWORDS['cjardin']

@app.route('/buy') #endpoint
def buy():
    return 'Buy'

@app.route('/hello') #endpoint
def hello():
    return render_template('hello.html',img_url=IMGS_URL[CUR_ENV] ) 

@app.route('/back',  methods=['GET']) #endpoint
def back():
    return render_template('backatu.html',input_from_browser=request.args.get('usay', default = "nothing", type = str) )

@app.route('/backp',  methods=['POST']) #endpoint
def backp():
    print(request.form)
    salted = bcrypt.hashpw( bytes(request.form['fname'],  'utf-8' ) , bcrypt.gensalt(10))
    print(salted)

    print(  bcrypt.checkpw(  bytes(request.form['fname'],  'utf-8' )  , salted ))

    return render_template('backatu.html',input_from_browser= str(request.form) )

@app.route('/auth',  methods=['POST']) #endpoint
def auth():
        print(request.form)
        return json_response(data=request.form)



#Assigment 2
@app.route('/ss1') #endpoint
def ss1():
    return render_template('server_time.html', server_time= str(datetime.datetime.now()) )

@app.route('/getTime') #endpoint
def get_time():
    return json_response(data={"password" : request.args.get('password'),
                                "class" : "cis44",
                                "serverTime":str(datetime.datetime.now())
                            }
                )
#Assignment 3

@app.route('/', methods = ['GET'])
def userLoginPage():
    return render_template('userLoginForm.html')

def acceptedToken(token):
    if TOKEN is None:
        print("There is no token")
        return False
    else:
        serverToken = decodingToken(TOKEN)
        clientToken = decodingToken(token)

        return True if serverToken == clientToken else False

def decodingToken(token):
    return jwt.decode(token, JWT_SECRET, algorithms = ["HS256"])

@app.route('/login', methods = ['POST'])
def authorizeUser():
    cur = global_db_con.cursor()
    cur.execute("select * from users where username = '%s';" % (request.form['username']))
    db_row = cur.fetchone()

    if db_row is None:
        print("The username '" + request.form['username'] + "' is invalid or does not exist.")
        return json_response(data={"message": "The username '" + request.form['username'] + "' is invalid or does not exist."}, status=404)
    else:
        if request.form['password'] == db_row[2]: #change maybe
            print(request.form['username'] + " has succussfully logged in.")
            global TOKEN
            TOKEN = jwt.encode({"user_id": db_row[0]}, JWT_SECRET, algorithm="HS256")
            return json_response(data={"jwt": TOKEN})
        else:
            print('The password for ' + request.form['username'] + ' is incorrect.')
            return json_response(data={"message": "The password for '" + request.form['username'] + "' is incorrect."}, status=404)
        
@app.route('/getbooks', methods = ['POST'])
def getBooks():
    if acceptedToken(request.form['jwt']) == True:
        #print("Token accepted! .....Showing available books")
        cur = global_db_con.cursor()

        try:
            cur.execute("select * from books;")
            print("books retrieved")
        except:
            print("books unable to be found")
            return json_response(data={"message": "books unable to be found."}, status=500)

        message = "{\"books\":["
        bookCounter = 0
        
        while True:
            db_row = cur.fetchone()

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

    else:
        print("Token Invalid.")
        return json_response(data={"message": "Token Invalid."}, status=404)
    

@app.route('/auth2') #endpoint
def auth2():
    jwt_str = jwt.encode({"username" : "cary",
                            "age" : "so young",
                            "books_ordered" : ['f', 'e'] } 
                            , JWT_SECRET, algorithm="HS256")
    #print(request.form['username'])
    return json_response(jwt=jwt_str)

@app.route('/exposejwt') #endpoint
def exposejwt():
    jwt_token = request.args.get('jwt')
    print(jwt_token)
    return json_response(output=jwt.decode(jwt_token, JWT_SECRET, algorithms=["HS256"]))


@app.route('/hellodb') #endpoint
def hellodb():
    cur = global_db_con.cursor()
    cur.execute("insert into music values( 'dsjfkjdkf', 1);")
    global_db_con.commit()
    return json_response(status="good")


app.run(host='0.0.0.0', port=80)

