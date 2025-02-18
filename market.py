from app import app, db
import sqlalchemy
import sqlalchemy.orm as so
from app.models import User, Post

@app.shell_context_processor
def maker_shell_context():
    return {'sa': sqlalchemy, 'so': so, 'db': db, 'User': User, 'Post': Post}
