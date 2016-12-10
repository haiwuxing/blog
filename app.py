import os;
from flask import Flask;
from flask_sqlalchemy import SQLAlchemy;

app = Flask(__name__)
app.config.from_object(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='admin',
));

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db';
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True;

db = SQLAlchemy(app);

# import all of our routes from routes.py
#from views import *;

if __name__ == '__main__':
    app.run(debug=True);
