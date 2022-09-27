import email
from flask import Flask, render_template, request, flash, redirect, session, abort, g
import requests
from forms import LoginForm, SearchForm, RegisterForm
from models import db, connect_db, User
from sqlalchemy.exc import IntegrityError
from private import password, private_key, API_KEY

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:{password}@localhost:5432/locations'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = f'{private_key}'

connect_db(app)
db.create_all()


# Send request to API ------------------------------------------------------------


# res = requests.get(f'http://api.ipstack.com/{ip_address}?access_key={API_KEY}')


# User Signup/Login/Logout --------------------------------------------------


@app.before_request
def add_user_to_g():

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):

    session[CURR_USER_KEY] = user.id


def do_logout():

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]



# Routes -----------------------------------------------------------------


@app.route('/')
def homepage():

    # # if not g.user:
    # #     flash("Please log in or sign up to search!", "danger")
    # #     return redirect("/login")
    
    # # user = g.user
    # form = SearchForm()

    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)
    
        if user:
            do_login(user)
            flash(f"Welcome back, {user.username}", "success")
            return redirect('/')
    
        flash("Username or Password is incorrect.", "danger")
    
    return render_template('users/login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def signup():

    form = RegisterForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data
            )
            db.session.commit()
    
        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('users/register.html', form=form)
    
        do_login(user)

        return redirect('/')

    else:
        return render_template('users/register.html', form=form)


@app.route('/logout')
def log_user_out():
    do_logout()

    return redirect('/login')