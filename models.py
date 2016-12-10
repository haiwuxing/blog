'''
Models for post
'''

import time;
from datetime import date;


class Post1(object):
    """代表一篇博文"""
    def __init__(self, id=None, title=None, text=None):
        self.title = title;
        self.text = text;
        self.created_at = time.time();

    @property
    def created_at(self):
        dt = date.fromtimestamp(self.__created_at);
        return '%s年%s月%s日' % (dt.year, dt.month, dt.day);

    @created_at.setter
    def created_at(self, created_at):
        self.__created_at = created_at;

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

# 一些测试代码
if __name__ == '__main__':
    db.create_all();
    #post = Post('aaa','111');
    #print(post.created_at);
