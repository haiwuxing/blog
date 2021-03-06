from flask import Flask;

# static_url_path="" serve static file in static folder.
app = Flask(__name__, static_url_path="");
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
    # 多线程，可以提高 AngularJS App 访问的速度。
    app.run(debug=True, threaded=True);
