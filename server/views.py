from flask import Flask, render_template, request, flash, url_for, redirect,\
    session, jsonify;
from app import app;
from models import *;
from serializers import PostSerializer;

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

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
    posts = Post.query.order_by(Post.created_at.desc());
    print(type(posts));
    print("posts1={}" % posts);
    return render_template('index.html', posts = posts);

# Retrieve a post.
@app.route('/retrieve/<int:post_id>', methods=['GET'] )
def show_post(post_id):
    """Show a post"""
    # show the post with the given id, the id is an integer
    post = Post.query.get(post_id);
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
        post = Post(request.form['title'], request.form['body']);
        db.session.add(post);
        db.session.commit();
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
        post = Post.query.get(post_id);
        return render_template('update_post.html', post = post);
    elif request.method == 'POST':
        post = Post.query.get(post_id);
        post.title = request.form['title'];
        post.body = request.form['body'];
        db.session.commit();
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
    post = Post.query.get(post_id);
    db.session.delete(post);
    db.session.commit();
    flash('Post was deleted');
    return redirect(url_for('index'));


# API
# GET:  http://[hostname]/api/v1.0/posts: Retrieve list of posts
# GET:  http://[hostname]/api/v1.0/posts/[task_id]: Retrieve a post
# POST: http://[hostname]/api/v1.0/posts: Create a new post
# PUT:  http://[hostname]/api/v1.0/posts/[task_id]: Update an existing post
# DELETE: http://[hostname]/api/v1.0/posts/[task_id]: Delete a post

@app.route('/api/v1.0/posts/', methods=['GET'])
def get_posts():
    posts = Post.query.order_by(Post.created_at.desc());
    schema = PostSerializer();
    data, errors = schema.dump(posts, many=True);
    return jsonify({"posts": data});

@app.route('/api/v1.0/posts/<int:post_id>', methods=['GET'])
def get_a_post(post_id):
    #post = Post.query.get(post_id);
    post = Post.query.filter_by(id=post_id).first();
    schema = PostSerializer();
    data, errors = schema.dump(post);
    return jsonify({"post":data});