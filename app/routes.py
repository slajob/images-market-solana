from flask import render_template
from app import app

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
