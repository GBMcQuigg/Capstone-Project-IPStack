
from flask import Flask, render_template, flash, redirect, session, g
import requests
from forms import LoginForm, SearchForm, RegisterForm
from models import db, connect_db, User, Result
from sqlalchemy.exc import IntegrityError
# from private import password, private_key, API_KEY, API_BASE_URL
import os

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', f'postgresql://postgres:@localhost:5432/locations')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 1391)

connect_db(app)
db.create_all()



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

    
@app.route('/register', methods=['GET', 'POST'])
def signup():

    form = RegisterForm()

    if form.validate_on_submit():
        try:
            new_user = User.signup(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data
            )
            db.session.commit()
            session['user_id'] = new_user.id

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('users/register.html', form=form)
    
        do_login(new_user)

        return redirect('/')

    else:
        return render_template('users/register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)
    
        if user:
            do_login(user)
            flash(f"Welcome back, {user.username}", "success")
            session['user_id'] = user.id
            return redirect('/')
    
        flash("Username or Password is incorrect.", "danger")
    
    return render_template('users/login.html', form=form)




@app.route('/logout')
def log_user_out():

    do_logout()

    flash("You have been successfully logged out.", "success")

    return redirect('/login')



# Routes -----------------------------------------------------------------


@app.route('/')
def location_response():

    if "curr_user" not in session:
        flash("You must login or sign up to proceed.", "danger")
        return redirect('/login')

    form = SearchForm()

    return render_template('home.html', form=form)


@app.route('/', methods=["POST"])
def homepage():

    if "curr_user" not in session:
        flash("You must login or sign up to proceed.", "danger")
        return redirect('/login')

    form = SearchForm()

    if form.validate_on_submit():
        
        search = form.search.data
        
        res = requests.get(f'http://api.ipstack.com/{search}?access_key=8d88396fbf7b759b8602b0e0cf2b8b41')
        data = res.json()
        city = data['city']
        state = data['region_name']
        country = data['country_name']
        location = {'city': city, 'state': state, 'country': country}

        new_search = Result(searchLocation=search, userId=session["curr_user"])
        db.session.add(new_search)
        db.session.commit()

        return render_template('location.html', form=form, location=location)
    
    # flash("Error: Invalid IP Address.", "danger")
    return render_template('home.html', form=form)
    