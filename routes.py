from flask import Flask, render_template;
from app import app;
from models import *;

@app.route('/')
def hello():
    """Renders a sample page."""
    posts = [];
    post1 = Post(id=1,title="标题1", text="content1", created_at="2015-01-01");
    post2 = Post(id=2,title="标题2", text="content2", created_at="2015-01-02");
    posts.append(post1);
    posts.append(post2);
    return render_template('index.html', posts = posts);