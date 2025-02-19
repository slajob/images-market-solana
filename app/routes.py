from flask import render_template, flash, redirect, url_for
from app import app, db
from app.forms import LoginForm, RegisterForm, EmptyForm, PostForm
from app.models import User, Post
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy
from time import time

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('You just posted!')
        return redirect(url_for('index'))
    posts = db.session.scalars(sqlalchemy.select(Post).order_by(Post.timestamp.desc())).all()
    return render_template('index.html', title='Home', posts=posts, form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sqlalchemy.select(User).where(User.username == form.username.data))
        if user is None or not user.validate_password(form.password.data):
            flash('Wrong username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You are now registered!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = db.first_or_404(sqlalchemy.select(User).where(User.username == username))
    posts = [
        {'author': user, 'body': 'post 1'},
        {'author': user, 'body': 'post 1'}
    ]
    form = EmptyForm()
    return render_template('user.html', user=user, posts=posts, form=form)

@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = db.session.scalar(sqlalchemy.select(User).where(User.username == username))
        if user is None:
            flash(f'User {username} not found')
            return redirect(url_for('index'))
        if user == current_user:
            flash(f'You cannot follow yourself dummy')
            return redirect(url_for('user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash(f'You are now following {username}')
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))

@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = db.session.scalar(sqlalchemy.select(User).where(User.username == username))
        if user is None:
            flash(f'404: User {username} not found')
            return redirect(url_for('index'))
        if user == current_user:
            flash(f'You cannot unfollow yourself dummy')
            return redirect(url_for('user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash(f'You Are not following {username}')
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))
