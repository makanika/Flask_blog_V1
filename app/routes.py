from flask_login import current_user, login_user, logout_user, login_required, login_remembered
from flask import render_template, flash, redirect, url_for, request
from urllib.parse import urlsplit
from app import app
from app.forms import LoginForm
from app.models import User
import sqlalchemy as sa
from app import db


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
            'lead':'Finding and Enjoying Mathmatics in a musical environment',
            'body':'Uganda can be a challenging place to express yourself and grow'
        },
        {
            'author':{'username':'Flavia Nanyanzi'},
            'lead':'Finding and Enjoying Mathmatics in a musical environment',
            'body':'Uganda can be a challenging place to express yourself and grow'
        },
        {
            'author':{'username':'Solomon Kamukama'},
            'lead':'Finding and Enjoying Mathmatics in a musical environment',
            'body':'Uganda can be a challenging place to express yourself and grow'
        },
        {
            'author':{'username':'Emannuel Engwaru'},
            'lead':'Finding and Enjoying Mathmatics in a musical environment',
            'body':'Uganda can be a challenging place to express yourself and grow'
        },
        {
            'author':{'username':'Daniel Akiki Birungi'},
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

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))