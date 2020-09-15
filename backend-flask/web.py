import flask

# print(__name__, __package__)

import os, sys
import time

from ..bin.parsers.wiktionary_parser_soup import get_wiktionary_word

app = flask.Flask(__name__)

@app.after_request
def add_header(response):
    # make sure no caching occurs
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    # response.headers['Cache-Control'] = 'public, max-age=0'
    return response

@app.route('/')
def hello_world():
    return flask.render_template('pages/index.html')

@app.route('/user')
def get_user():
    return 'Sasha'

@app.route('/users/')
def get_users():
    return 'Spisok'

@app.route('/user/<username>')
def get_user_by_name(username):
    return f'A, eto {username}. Etogo pidora v himkah vidal'

@app.route('/words/<word>')
def get_word(word):
    word_dict = get_wiktionary_word(word)
    return flask.render_template('pages/words/word.html', word_name=word, word_dict=word_dict) if word_dict else f'No such word {word}'

@app.route('/time')
def get_current_time():
    return {'time': time.time(), 'mrazi': 'borodati'}

# with app.test_request_context():
#     print(flask.url_for('hello_world'))
#     print(flask.url_for('get_user'))
#     print(flask.url_for('get_users', next='/'))
#     print(flask.url_for('get_user_by_name', username='John Doe'))
#     print(flask.url_for('static', filename='styles/style.css'))