from flask import Flask, render_template, request, flash, url_for, redirect;
from app import app;
from models import *;
from orm import *;

@app.route('/')
def index():
    """Index"""
    db = get_db();
    cur = db.execute('select id, title, text, created_at from posts order by id desc');
    posts = cur.fetchall();
    # print(posts[0]['title']); // ok
    # print(posts[0].title); // not ok
    return render_template('index.html', posts = posts);

# Retrieve a post.
@app.route('/post/<int:post_id>', methods=['GET'] )
def show_post(post_id):
    """Show a post"""
    # show the post with the given id, the id is an integer
    db = get_db();
    cur = db.execute('select id, title, text, created_at from posts where id=?', [post_id]);
    post = cur.fetchone();
    return render_template('show_post.html', post = post);

# Create a post.
@app.route('/add', methods=['GET', 'POST'])
def add_post():
    if request.method == 'GET':
        return render_template('create_post.html');
    elif request.method== 'POST':
        post = Post();
        db = get_db();
        db.execute('insert into posts (title, text, created_at) values (?,?,?)',
                    [request.form['title'],
                    request.form['text'],
                    post.created_at]);
        db.commit()
        flash('New post was successfully posted')
        return redirect(url_for('index'));

# Update a post.

# Delete a post.
    