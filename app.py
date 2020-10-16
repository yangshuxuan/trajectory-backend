from flask import Flask
from datetime import datetime
import re
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
from flask import Flask

from database import postsqldb
from flask_restful import Api
from geoalchemy2.elements import WKTElement
from resources.routes import initialize_routes
import os
from flask_cors import CORS
from admin import flaskadmin
app = Flask(__name__)
CORS(app)
api = Api(app)
app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://localhost/movie-bag'
}

# get environment variables
dbAddr = os.environ.get("DBADDR")
dbPort = os.environ.get("DBPORT")
dbUser = os.environ.get("DBUSER")
dbPass = os.environ.get("DBPASS")
assert(dbAddr)
assert(dbPort)
assert(dbUser)
assert(dbPass)

dbURL= "postgresql://" + dbUser + ":" + dbPass + "@" + dbAddr + ":" + dbPort + "/nyc"

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("nyc", dbURL)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_BINDS'] = {
    'nyc':        os.environ.get("nyc", dbURL)
}

postsqldb.db.initialize_db(app)




flaskadmin.initialize_admin(app)
initialize_routes(api)
@app.route("/")
def home():
    return "Hello, Flask!"
@app.route("/hello/<name>")
def hello_there(name):
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X")

    # Filter the name argument to letters only using regular expressions. URL arguments
    # can contain arbitrary text, so we restrict to safe characters only.
    match_object = re.match("[a-zA-Z]+", name)

    if match_object:
        clean_name = match_object.group(0)
    else:
        clean_name = "Friend"

    content = "Hello there, " + clean_name + "! It's " + formatted_now
    return content


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)