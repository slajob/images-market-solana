from typing import Optional
import sqlalchemy
import sqlalchemy.orm as so
from app import db, login
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5

followers = sqlalchemy.Table(
    'followers',
    db.metadata,
    sqlalchemy.Column('follower_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('user.id'), primary_key=True),
    sqlalchemy.Column('followed_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('user.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sqlalchemy.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sqlalchemy.String(128), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sqlalchemy.String(256))
    posts: so.WriteOnlyMapped['Post'] = so.relationship(back_populates='author')
    following: so.WriteOnlyMapped['User'] = so.Relationship(secondary=followers,
                                                            primaryjoin=(followers.c.follower_id == id),
                                                            secondaryjoin=(followers.c.followed_id == id),
                                                            back_populates='followers')
    followers: so.WriteOnlyMapped['User'] = so.relationship(secondary=followers,
                                                            primaryjoin=(followers.c.followed_id == id),
                                                            secondaryjoin=(followers.c.follower_id == id),
                                                            back_populates='following')

    def __repr__(self):
        return '<User {}'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        dig = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{dig}?d=identicon&s={size}'

    def follow(self, user):
        if not self.is_following(user):
            self.following.add(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.following.remove(user)

    def is_following(self, user):
        query = self.following.select().where(User.id == user.id)
        return db.session.scalar(query) is not None

    def followers_count(self):
        query = sqlalchemy.select(sqlalchemy.func.count().select_from(self.followers.select().subquery()))
        return db.session.scalar(query)

    def following_count(self):
        query = sqlalchemy.select(sqlalchemy.func.count().select_from(self.following.select().subquery()))
        return db.session.scalar(query)

class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sqlalchemy.String(256))
    timestamp: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    user_id: so.Mapped[int] = so.mapped_column(sqlalchemy.ForeignKey(User.id), index=True)
    author: so.Mapped[User] = so.relationship(back_populates='posts')

    def __repr__(self):
        return '<Post {}'.format(self.body)


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

