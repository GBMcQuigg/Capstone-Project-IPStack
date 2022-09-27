from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()



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





    @classmethod
    def signup(cls, username, email, password):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
        )

        db.session.add(user)
        return user


    @classmethod
    def authenticate(cls, username, password):
        """Find user with username and password."""

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


def connect_db(app):
    """Connect this database to provided Flask app."""

    db.app = app
    db.init_app(app)