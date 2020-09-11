import flask
import os, sys
# sys.path.clear()
# sys.path.remove('/home/sha-dou/projects')
# sys.path.remove('/home/sha-dou/projects/3Words/venv-linux/bin')
# sys.path.remove('/usr/lib/python38.zip')
# sys.path.remove('/usr/lib/python3.8/lib-dynload')
# print(os.getcwd())
# print(sys.path)
# print(__name__, __package__)
from ..bin.parsers.wiktionary_parser_soup import get_wiktionary_word
# print(get_wiktionary_word('ass'))
app = flask.Flask(__name__)

@app.after_request
def add_header(response):
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

# with app.test_request_context():
#     print(flask.url_for('hello_world'))
#     print(flask.url_for('get_user'))
#     print(flask.url_for('get_users', next='/'))
#     print(flask.url_for('get_user_by_name', username='John Doe'))
#     print(flask.url_for('static', filename='styles/style.css'))