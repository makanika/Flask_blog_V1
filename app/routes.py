from flask_login import current_user, login_user, logout_user, login_required, login_remembered
from flask import render_template, flash, redirect, url_for, request
from urllib.parse import urlsplit
from datetime import datetime, timezone
from app import app
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from app.models import User
import sqlalchemy as sa
from app import db

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/blog')
@login_required
def blog():
    posts = [
        {
            'author':{'username':'Joan Nantambi'},
            'title':'Finding God and Living Christianity in the modern workplace',
            'lead':'Finding God and Living Christianity in the modern workplace',
            'body':'Uganda can be a challenging place to express yourself and grow'
        },
        {
            'author':{'username':'Flavia Nanyanzi'},
            'title':'Sexaul Harrasment and Navigating it in the workplace',
            'lead':'Finding and Enjoying Mathmatics in a musical environment',
            'body':'Uganda can be a challenging place to express yourself and grow'
        },
        {
            'author':{'username':'Solomon Kamukama'},
            'title':'Being Led and Being Humble enough to be led',
            'lead':'Finding and Enjoying Mathmatics in a musical environment',
            'body':'Uganda can be a challenging place to express yourself and grow'
        },
        {
            'author':{'username':'Emannuel Engwaru'},
            'title':'The Challenge of having a supervisor that is SuperMan',
            'lead':'Finding and Enjoying Mathmatics in a musical environment',
            'body':'Uganda can be a challenging place to express yourself and grow'
        },
        {
            'author':{'username':'Daniel Akiki Birungi'},
            'title':'Navigating Leadership while Leading Professionals',
            'lead':'Finding and Enjoying Mathmatics in a musical environment',
            'body':'Uganda can be a challenging place to express yourself and grow'
        }
    ]
    return render_template('blog.html', title='blog', posts=posts)

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid Username OR Password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc !='':
            next_page = url_for('blog')
        return redirect(next_page)
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('blog'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations You are Now a Registered User')
        return redirect(url_for('login'))
    return render_template('register.html', title='Sign Up', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/user/<username>')
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(username == username))
    posts = [
        {'author': user, 'body': 'Test Post from the router #1'},
        {'author': user, 'body': 'Test Post from the router #2'},
        {'author': user, 'body': 'Test Post from the router #3'},
        {'author': user, 'body': 'Test Post from the router #4'},
    ]
    return render_template('user.html', user=user, posts=posts)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    # Instantiate the form without arguments for simplicity
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your profile has been updated!')
        # Redirect to the user's profile page to see the changes
        return redirect(url_for('user', username=current_user.username))
    elif request.method == 'GET':
        # This now correctly populates the form with the user's current data
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)


