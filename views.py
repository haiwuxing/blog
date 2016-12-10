from flask import Flask, render_template, request, flash, url_for, redirect,\
    session;
from app import app;
from models import *;
from orm import *;

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)
 
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))

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
@app.route('/retrieve/<int:post_id>', methods=['GET'] )
def show_post(post_id):
    """Show a post"""
    # show the post with the given id, the id is an integer
    db = get_db();
    cur = db.execute('select id, title, text, created_at from posts where id=?',
                     [post_id]);
    post = cur.fetchone();
    return render_template('show_post.html', post = post);

# Create a post.
@app.route('/add', methods=['GET', 'POST'])
def add_post():
    if not ('logged_in' in session):
        flash('还没有登陆');
        return redirect(url_for('index'));
    if request.method == 'GET':
        return render_template('create_post.html');
    elif request.method== 'POST':
        post = Post();
        db = get_db();
        db.execute('insert into posts (title, text, created_at) values (?,?,?)',
                    [request.form['title'],
                    request.form['text'],
                    post.created_at]);
        db.commit();
        flash('New post was successfully posted')
        return redirect(url_for('index'));

# Update a post.
@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update_post(post_id):
    """Update a post"""
    if not ('logged_in' in session):
        flash('还没有登陆');
        return redirect(url_for('index'));
    if request.method == 'GET':
        db = get_db();
        cur = db.execute('select id, title, text, created_at from posts where id=?',
                         [post_id]);
        post = cur.fetchone();
        return render_template('update_post.html', post = post);
    elif request.method == 'POST':
        db = get_db();
        db.execute('UPDATE posts SET title = ?, text = ? WHERE id = ?',
                   (request.form['title'], request.form['text'], post_id));
        db.commit();
        flash('文章更新成功');
        return redirect(url_for('show_post', post_id = post_id));
    else:
        abort('404')

# Delete a post.
@app.route('/delete/<int:post_id>', methods=['GET'])
def delete_post(post_id):
    """Delete a post"""
    if not ('logged_in' in session):
        flash('还没有登陆');
        return redirect(url_for('index'));
    db = get_db();
    db.execute('DELETE FROM posts WHERE id=?', [post_id]);
    db.commit();
    flash('Post was deleted');
    return redirect(url_for('index'));
    