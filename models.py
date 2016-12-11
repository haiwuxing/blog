'''
Models for post
'''
from app import app;
from flask_sqlalchemy import SQLAlchemy;
import datetime;

db = SQLAlchemy(app);

class Post(db.Model):
    __tablename__='posts';

    id = db.Column(db.Integer, primary_key=True);
    title = db.Column(db.String);
    body = db.Column(db.Text);
    # TODO: 去掉毫秒“2016-12-11 10:11:56.717962”
    # efault=db.func.now(), 不会识别时区。
    created_at =  db.Column(db.DateTime, default=datetime.datetime.now());

    def __init__(self, title, body):
        self.title = title;
        self.body = body;
    
    def __repr__(self):
        return '<Post> %r>' % self.title;

# 一些测试代码
if __name__ == '__main__':
    post = Post('aaa','111');
    print(post.created_at);
