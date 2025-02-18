from flask import render_template, flash, redirect, url_for
from app import app, db
from app.forms import LoginForm
from app.models import User
from flask_login import current_user, login_user, logout_user
import sqlalchemy

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'slajob'}
    posts = [
        {
            'author': {'username': 'slajob'},
            'body': 'Check my image and boost me!'
        },
        {
            'author': {'username': 'Lola'},
            'body': 'My latest job is out, check it out!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sqlalchemy.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Wrong username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))