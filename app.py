# -*- coding: utf-8 -*-
"""
    flask-see example
    ~~~~~~~~~~~~~~~~~~

    :author: Grey Li
    :copyright: © 2018 Grey Li
    :license: MIT, see LICENSE for more details.
"""
from flask import Flask, render_template, redirect, url_for, request
from flask_sse import sse
from gevent.pywsgi import WSGIServer
from faker import Faker

fake = Faker()

app = Flask(__name__)
app.config['REDIS_URL'] = 'redis://localhost'

app.register_blueprint(sse, url_prefix='/stream')


@app.route('/')
def index():
    return render_template('lobby.html')


@app.route('/darkroom')
def darkroom():
    return render_template('darkroom.html')


@app.route('/knock', methods=['GET', 'POST'])
def knock():
    if request.method == 'POST':
        username = request.form.get('username', 'Someone')
        sse.publish({'username': username}, type='knock')
        return redirect(url_for('knock'))

    username = fake.name()
    return render_template('knock.html', username=username)


@app.route('/hello/<username>')
def hello(username):
    sse.publish({'message': 'hi'}, channel='%s' % username)
    return redirect(url_for('index'))


@app.route('/user/<username>')
def user(username):
    return render_template('user.html', username=username)


http_server = WSGIServer(('', 5000), app)
http_server.serve_forever()
