from flask import Flask;

app = Flask(__name__)
app.config.from_object(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='admin',
));

# TODO: 怎样通过绝对路径////指定。
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db';
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True;

# import all of our routes from routes.py
from views import *;

if __name__ == '__main__':
    app.run(debug=True);
