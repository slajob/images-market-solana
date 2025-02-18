from typing import Optional
import sqlalchemy
import sqlalchemy.orm as so
from app import db
from datetime import datetime, timezone

class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sqlalchemy.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sqlalchemy.String(128), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sqlalchemy.String(256))
    posts: so.WriteOnlyMapped['Post'] = so.relationship(back_populates='author')

    def __repr__(self):
        return '<User {}'.format(self.username)

class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sqlalchemy.String(256))
    timestamp: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    user_id: so.Mapped[int] = so.mapped_column(sqlalchemy.ForeignKey(User.id), index=True)
    author: so.Mapped[User] = so.relationship(back_populates='posts')

    def __repr(self):
        return '<Post {}'.format(self.body)