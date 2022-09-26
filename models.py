from datetime import datetime

# from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

# bcrypt = Bcrypt()
db = SQLAlchemy()

class User(db.Model):
    """User saved to the database."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    
    username = db.Column(
        db.Text,
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.Text,
        nullable=False
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True
    )


class Result(db.Model):
    """Stored results from user search queries."""

    __tablename__ = 'results'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    searchLocation = db.Column(
        db.Text,
        nullable=False
    )

    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow()
    )

    userId = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False
    )


def connect_db(app):
    """Connect this database to provided Flask app."""

    db.app = app
    db.init_app(app)