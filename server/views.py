from flask import Flask, render_template, request, flash, url_for, redirect,\
    session, jsonify, abort, make_response;
from app import app;
from models import *;
from serializers import PostSerializer;
from flask_httpauth import HTTPBasicAuth;

auth = HTTPBasicAuth();

@auth.get_password
def get_password(username):
    if username == 'jian':
        return 'python'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401);

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

#@app.route('/login', methods=['GET', 'POST'])
#def login():
#    error = None
#    if request.method == 'POST':
#        if request.form['username'] != app.config['USERNAME']:
#            error = 'Invalid username'
#        elif request.form['password'] != app.config['PASSWORD']:
#            error = 'Invalid password'
#        else:
#            session['logged_in'] = True
#            flash('You were logged in')
#            return redirect(url_for('index'))
#    return render_template('login.html', error=error)
 
#@app.route('/logout')
#def logout():
#    session.pop('logged_in', None)
#    flash('You were logged out')
#    return redirect(url_for('index'))

#@app.route('/')
#def index():
#    """Index"""
#    posts = Post.query.order_by(Post.created_at.desc());
#    print(type(posts));
#    print("posts1={}" % posts);
#    return render_template('index.html', posts = posts);

## Retrieve a post.
#@app.route('/retrieve/<int:post_id>', methods=['GET'] )
#def show_post(post_id):
#    """Show a post"""
#    # show the post with the given id, the id is an integer
#    post = Post.query.get(post_id);
#    return render_template('show_post.html', post = post);

## Create a post.
#@app.route('/add', methods=['GET', 'POST'])
#def add_post():
#    if not ('logged_in' in session):
#        flash('还没有登陆');
#        return redirect(url_for('index'));
#    if request.method == 'GET':
#        return render_template('create_post.html');
#    elif request.method== 'POST':
#        post = Post(request.form['title'], request.form['body']);
#        db.session.add(post);
#        db.session.commit();
#        flash('New post was successfully posted')
#        return redirect(url_for('index'));

### Update a post.
##@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
##def update_post(post_id):
##    """Update a post"""
##    if not ('logged_in' in session):
##        flash('还没有登陆');
##        return redirect(url_for('index'));
##    if request.method == 'GET':
##        post = Post.query.get(post_id);
##        return render_template('update_post.html', post = post);
##    elif request.method == 'POST':
##        post = Post.query.get(post_id);
##        post.title = request.form['title'];
##        post.body = request.form['body'];
##        db.session.commit();
##        flash('文章更新成功');
##        return redirect(url_for('show_post', post_id = post_id));
##    else:
##        abort('404')

## Delete a post.
#@app.route('/delete/<int:post_id>', methods=['GET'])
#def delete_post(post_id):
#    """Delete a post"""
#    if not ('logged_in' in session):
#        flash('还没有登陆');
#        return redirect(url_for('index'));
#    post = Post.query.get(post_id);
#    db.session.delete(post);
#    db.session.commit();
#    flash('Post was deleted');
#    return redirect(url_for('index'));


# API
# GET:  http://[hostname]/api/v1.0/posts: Retrieve list of posts
# GET:  http://[hostname]/api/v1.0/posts/[task_id]: Retrieve a post
# POST: http://[hostname]/api/v1.0/posts: Create a new post
# PUT:  http://[hostname]/api/v1.0/posts/[task_id]: Update an existing post
# DELETE: http://[hostname]/api/v1.0/posts/[task_id]: Delete a post

#@auth.error_handler
#def unauthorized():
#    return make_response(jsonify( { 'error': 'Unauthorized access' } ), 403)
#    # return 403 instead of 401 to prevent browsers from displaying the default auth dialog

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad request'}), 400);

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404);

# generates a "public" version of a post to send to the client
def make_public_post(post):
    new_post = {};
    for field in post:
        if field == 'id':
            new_post['uri'] = url_for('get_post', post_id=post['id'], _external=True);
        else:
            new_post[field] = post[field];
    return new_post;

# GET:  http://[hostname]/api/v1.0/posts: Retrieve list of posts
# POST: http://[hostname]/api/v1.0/posts: Create a new post
@app.route('/api/v1.0/posts', methods=['GET'])
def get_posts():
    if request.method == 'GET':
        posts = Post.query.order_by(Post.created_at.desc());
        schema = PostSerializer();
        data, errors = schema.dump(posts, many=True);
        return jsonify({"posts": [make_public_post(post) for post in data]});
        #return jsonify({"posts": map(make_public_post, posts)});
    elif request.method == 'POST':
        if not request.json or not 'title' in request.json or not 'body' in request.json:
            abort(404);
        post = Post(request.json['title'], request.json['body']);
        db.session.add(post);
        db.session.commit();
        # 查询并返回。
        post = Post.query.get(post.id);
        schema = PostSerializer();
        data, errors = schema.dump(post);
        return jsonify(data);
    else:
        abort(404);
    

# GET:  http://[hostname]/api/v1.0/posts/[task_id]: Retrieve a post
@app.route('/api/v1.0/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.get(post_id);
    if (post == None):
        abort(404);
    schema = PostSerializer();
    data, errors = schema.dump(post);
    return jsonify({'post':make_public_post(data)});

@app.route('/api/v1.0/posts', methods=['POST'])
@auth.login_required
def create_post():
    # 400: bad request
    if not request.json or not 'title' in request.json or not 'body' in request.json:
        abort(400);
    post = Post(request.json['title'], request.json['body']);
    db.session.add(post);
    db.session.commit();
    # 查询并返回。
    post = Post.query.get(post.id);
    schema = PostSerializer();
    data, errors = schema.dump(post);
    return jsonify({'post': make_public_post(data)}), 201;

@app.route('/api/v1.0/posts/<int:post_id>', methods=['PUT'])
@auth.login_required
def update_post(post_id):
    post = Post.query.get(post_id);
    if post == None:
        abort(404);
    if not request.json:
        abort(404);
    if 'title' in request.json and type(request.json['title']) != str:
        abort(400);
    if 'body' in request.json and type(request.json['body']) != str:
        abort(400);
    post.title = request.json.get('title');
    post.body = request.json.get('body');
    db.session.commit();

    # 查询并返回。
    post = Post.query.get(post.id);
    schema = PostSerializer();
    data, errors = schema.dump(post);
    return jsonify({'post': make_public_post(data)});

@app.route('/api/v1.0/posts/<int:post_id>', methods=['DELETE'])
@auth.login_required
def delte_post(post_id):
    post = Post.query.get(post_id);
    if post == None:
        abort(404);
    db.session.delete(post);
    db.session.commit();
    return jsonify({'result' : True});