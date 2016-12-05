'''
Models for post
'''

import time;
from datetime import date;

class Post(object):
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

# 一些测试代码
if __name__ == '__main__':
    post = Post();
    print(post.created_at);
