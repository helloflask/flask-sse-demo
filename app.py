# -*- coding: utf-8 -*-
"""
    flask-see example
    ~~~~~~~~~~~~~~~~~~

    :author: Grey Li
    :copyright: © 2018 Grey Li
    :license: MIT, see LICENSE for more details.
"""
from flask import Flask, render_template, redirect, url_for, request, session
from flask_sse import sse
from faker import Faker

fake = Faker()

app = Flask(__name__)
app.secret_key = 'dev key'
app.config['REDIS_URL'] = 'redis://localhost'

app.register_blueprint(sse, url_prefix='/stream')


@app.route('/')
def index():
    username = fake.name()
    session['username'] = username
    return render_template('index.html', username=username)


@app.route('/lobby')
def lobby():
    return render_template('lobby.html')


@app.route('/darkroom')
def darkroom():
    return render_template('darkroom.html')


@app.route('/knock')
def knock():
    username = session.get('username', 'Someone')
    sse.publish({'username': username}, type='knock')
    return '', 204


@app.route('/sing')
def sing():
    username = session.get('username', 'Someone')
    sse.publish({'username': username}, type='sing')
    return '', 204


@app.route('/hello/<username>')
def hello(username):
    sse.publish({'message': 'hi'}, channel='%s' % username)
    return redirect(url_for('index'))


@app.route('/user/<username>')
def user(username):
    return render_template('user.html', username=username)

