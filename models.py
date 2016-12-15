'''
Models for post
'''
from app import app;
from flask_sqlalchemy import SQLAlchemy;
import datetime;
import time;

db = SQLAlchemy(app);

localtimezone = datetime.timezone(
    datetime.timedelta(seconds=-time.timezone),
    time.tzname[0]);
utctimezone = datetime.timezone.utc;

class Post(db.Model):
    __tablename__='posts';

    id = db.Column(db.Integer, primary_key=True);
    title = db.Column(db.String);
    body = db.Column(db.Text);
    # 存储的是 UTC 时间
    created_at =  db.Column(db.DateTime);

    def __init__(self, title, body, created_at=None):
        self.title = title;
        self.body = body;
        if created_at is None:
            created_at = datetime.datetime.utcnow();
        self.created_at = created_at;
    
    def __repr__(self):
        return '<Post> %r>' % self.title;

    # 将 created_at 转换为本地时间
    def local_created_at(self, fmt="%Y-%m-%d %H:%M:%S"):
        """ format utc datetime object as local datetime string"""
        return self.created_at.replace(tzinfo=utctimezone).\
            astimezone(localtimezone).strftime(fmt);

# 一些测试代码
if __name__ == '__main__':
    post = Post('aaa','111');
    print(post.created_at);
    db.session.add(post);
    db.session.commit();
    print(post.created_at);
    print(type(post.created_at));
    print(post.created_at.tzinfo);
    print(post.local_created_at());
