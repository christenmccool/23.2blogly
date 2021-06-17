"""Blogly application."""

from flask import Flask, render_template, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def show_home():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    posts = posts[:5]
    return render_template('index.html', posts=posts)

@app.route('/users')
def show_users():
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users.html', users=users)

@app.route('/users/<int:user_id>')
def show_user_details(user_id):
    user = User.query.get(user_id)
    return render_template('user-details.html', user=user)

@app.route('/users/new')
def add_user_form():
    return render_template('user-add-form.html')

@app.route('/users/new', methods=['POST'])
def add_user():
    first = request.form['first']
    last = request.form['last']
    url = request.form['url'] if request.form['url'] else None

    new_user = User(first_name = first, last_name = last, image_url = url)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')    

@app.route('/users/<int:user_id>/edit')
def edit_user_form(user_id):
    user = User.query.get(user_id)
    return render_template('user-edit-form.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
    first = request.form['first'] 
    last = request.form['last'] 
    url = request.form['url'] 

    user = User.query.get(user_id)
    user.first_name = first
    user.last_name = last
    user.image_url = url

    db.session.add(user)
    db.session.commit()

    return redirect('/users')   

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    
    return redirect('/users')   

@app.route('/users/<int:user_id>/posts/new')
def add_user_post_form(user_id):
    user = User.query.get(user_id)
    return render_template('user-add-post-form.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_post(user_id):
    title = request.form['title'] 
    content = request.form['content'] 

    post = Post(title=title, content=content, user_id=user_id)

    db.session.add(post)
    db.session.commit()
    return redirect(f"/users//{user_id}")  

@app.route('/posts/<int:post_id>')
def show_post_details(post_id):
    post = Post.query.get(post_id)
    return render_template('post-details.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def edit_post_form(post_id):
    post = Post.query.get(post_id)
    return render_template('post-edit-form.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post(post_id):
    post = Post.query.get(post_id)
    post.title = request.form['title'] 
    post.content = request.form['content'] 
    post.created_at = datetime.datetime.now()

    db.session.add(post)
    db.session.commit()
    return redirect(f"/posts/{post_id}")   

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = Post.query.filter_by(id=post_id).delete()
    db.session.commit()
    return redirect('/')