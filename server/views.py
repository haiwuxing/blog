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

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad request'}), 400);

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404);

# 将id  转换为 URI。
def make_public_post(post):
    new_post = {};
    for field in post:
        if field == 'id':
            new_post['uri'] = url_for('get_post', post_id=post['id'], _external=True);
        else:
            new_post[field] = post[field];
    return new_post;

#@auth.error_handler
#def unauthorized():
#    return make_response(jsonify( { 'error': 'Unauthorized access' } ), 403)
#    # return 403 instead of 401 to prevent browsers from displaying the default auth dialog

# API
# GET:  http://[hostname]/blog/api/v1.0/posts/: 获取文章列表
# GET:  http://[hostname]/blog/api/v1.0/posts/[task_id]: 读取一篇文章
# POST: http://[hostname]/blog/api/v1.0/posts: 创建一篇文章
# PUT:  http://[hostname]/blog/api/v1.0/posts/[task_id]: 更新一篇文章
# DELETE: http://[hostname]/blog/api/v1.0/posts/[task_id]: 删除一篇文章

# GET:  http://[hostname]/blog/api/v1.0/posts: 获取文章列表
@app.route('/blog/api/v1.0/posts/', methods=['GET'])
def get_posts():
    if request.method == 'GET':
        posts = Post.query.order_by(Post.created_at.desc());
        schema = PostSerializer();
        data, errors = schema.dump(posts, many=True);
        return jsonify({"posts": [make_public_post(post) for post in data]});
    

# GET:  http://[hostname]/blog/api/v1.0/posts/[task_id]: 读取一篇文章
@app.route('/blog/api/v1.0/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.get(post_id);
    if (post == None):
        abort(404);
    schema = PostSerializer();
    data, errors = schema.dump(post);
    return jsonify({'post':make_public_post(data)});

# POST: http://[hostname]/blog/api/v1.0/posts: 创建一篇文章
@app.route('/blog/api/v1.0/posts', methods=['POST'])
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

# PUT:  http://[hostname]/blog/api/v1.0/posts/[task_id]: 更新一篇文章
@app.route('/blog/api/v1.0/posts/<int:post_id>', methods=['PUT'])
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

# DELETE: http://[hostname]/blog/api/v1.0/posts/[task_id]: 删除一篇文章
@app.route('/blog/api/v1.0/posts/<int:post_id>', methods=['DELETE'])
@auth.login_required
def delte_post(post_id):
    post = Post.query.get(post_id);
    if post == None:
        abort(404);
    db.session.delete(post);
    db.session.commit();
    return jsonify({'result' : True});