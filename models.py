"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

# TODO: user default image url here
default_image = 'https://photolibrary.usap.gov/Tools/DrawImage.aspx?filename=emperor-penguin-noble.jpg'

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """User."""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.Text,
                     nullable=False)
    last_name = db.Column(db.Text,
                     nullable=False)
    image_url = db.Column(db.Text, 
                    nullable=False, 
                    default=default_image)
    
    posts = db.relationship('Post', backref='user')

    def __repr__(self):
        u = self
        return f"<User{u.id} {u.first_name} {u.last_name} {u.image_url}>"


class Post (db.Model):
    """ Post. """

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                    primary_key = True,
                    autoincrement=True)
    
    title = db.Column(db.Text,
                    nullable=False)
    
    content = db.Column(db.Text,
                        nullable=False)

    created_at = db.Column(db.DateTime,
                        nullable=False,
                        default=datetime.datetime.now)
                    
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'))

    def __repr__(self):
        p = self
        return f"<Post{p.id} {p.title} {p.content} {p.user_id}>"