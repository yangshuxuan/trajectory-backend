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

app = Flask(__name__)
api = Api(app)
app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://localhost/movie-bag'
}


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("nyc","postgresql://postgres:123456@localhost:5432/nyc")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



app.config['SQLALCHEMY_BINDS'] = {
    'nyc':        os.environ.get("nyc","postgresql://postgres:123456@localhost:5432/nyc")
}

postsqldb.db.initialize_db(app)

#db = SQLAlchemy(app)
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
    app.run(debug=True, host='0.0.0.0')