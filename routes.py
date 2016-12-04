from flask import Flask, render_template;
from app import app;
from models import *;

posts = [];
post1 = Post(id=1,title="标题1", text="content1", created_at="2015-01-01");
post2 = Post(id=2,title="标题2", text="content2", created_at="2015-01-02");
posts.append(post1);
posts.append(post2);

@app.route('/')
def index():
    """首页"""
    return render_template('index.html', posts = posts);

@app.route('/post/<int:post_id>', methods=['GET'] )
def show_post(post_id):
    """显示一篇博文"""
    # show the post with the given id, the id is an integer
    post = posts[post_id-1];
    return render_template('post.html', post = post);
