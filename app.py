from flask import Flask, render_template, request, flash, redirect, session, abort
from models import db, connect_db, User
from private import password, private_key

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:{password}@localhost:5432/locations'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = private_key

connect_db(app)
db.create_all()


@app.route('/')
def homepage():
    return render_template('home.html')