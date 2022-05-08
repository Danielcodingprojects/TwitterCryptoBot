from flask import render_template, url_for, redirect, flash, abort
from flask_login import LoginManager, login_user, login_required, current_user
from twitterbot import app, db
from twitterbot.forms import LoginForm, RegisterForm
from twitterbot.db_models import User
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from twitterbot.twitter_bot import Bot


login_manager = LoginManager()
login_manager.init_app(app)
bot = Bot()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def admin_only(func):
    @wraps(func)
    def decorated_func(*args, **kwargs):
        if not current_user.is_authenticated and current_user.get_id() != 1:
            return abort(403)
        return func(*args, **kwargs)
    return decorated_func


@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash("Username not found.")
            return redirect(url_for('/'))
        elif not check_password_hash(pwhash=user.password, password=password):
            flash('Password does not match.')
            return redirect(url_for('/'))
        else:
            login_user(user)
            return redirect(url_for('dashboard'))
    return render_template('index.html', form=form)


@app.route('/register_new_admin', methods=['GET', 'POST'])
@login_required
@admin_only
def register_admin():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        hashed_password = generate_password_hash(
            password=password,
            method="pbkdf2:sha256",
            salt_length=8
        )

        new_user = User(
            username=username,
            password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('register.html', form=form)


@app.route('/dashboard')
@login_required
def dashboard():
    # TODO; Make func that pulls these stats from DB
    follower_count = [100, 70, 90, 70, 85, 60, 75, 60, 90, 80, 110, 100]
    follower_dates = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
    return render_template('dashboard.html', follower_count=follower_count, follower_dates=follower_dates)
