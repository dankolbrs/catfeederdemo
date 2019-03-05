import os

from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash
from flask_bootstrap import Bootstrap

from .catfeeder import CatFeeder
from catfeeder.forms import LoginForm, FeedKitties

app = Flask(__name__)
Bootstrap(app)
app.config.from_object(__name__)
app.config.update(dict(
    SECRET_KEY=os.environ.get('SECRET_KEY'),
    USERNAME=os.environ.get('FLASK_USER'),
    PASSWORD=os.environ.get('FLASK_PASS'),
    DISABLE=os.environ.get('FLASK_FEEDER_DISABLE')))

TITLE = "CatFeeder"


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm()
    if form.validate_on_submit():
        session["name"] = form.username.data
        if form.password.data != app.config['PASSWORD']:
            flash('Invalid password')
        else:
            if not form.confirm.data:
                flash('Confirmation required')
            else:
                if not app.config['DISABLE']:
                    feeder = CatFeeder()
                    last_feed = feeder.get_last_feeding()
                    feeder.feed_cats(form.username.data)
                    print("fed")
                flash('William thanks you')
                return redirect(url_for('show_feed'))
    return render_template('login.html', error=error, form=form, title=TITLE)


@app.route('/logout')
def logout():
    return redirect(url_for('show_feed', title=TITLE))


@app.route('/', methods=['GET', 'POST'])
def show_feed():
    last_feed = None
    form = FeedKitties()
    if form.validate_on_submit() and not app.config['DISABLE']:
        feeder = CatFeeder()
        last_feed = feeder.get_last_feeding()
    return render_template('feed_kitties.html', last_feed_time=last_feed, form=form, title=TITLE)
