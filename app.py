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

class Post(db.Model):
    __tablename__='posts';

    id = db.Column(db.Integer, primary_key=True);
    title = db.Column(db.String);
    body = db.Column(db.Text);
    #created_at =  db.Column(db.DateTime, default=db.func.now());

    def __init__(self, title, body):
        self.title = title;
        self.body = body;
    
    def __repr__(self):
        return '<Post> %r>' % self.title;

# import all of our routes from routes.py
#from views import *;

if __name__ == '__main__':
    app.run(debug=True);
