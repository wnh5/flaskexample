# -*- coding:utf-8 -*-
#/usr/bin/python
#http://www.pythondoc.com/flask/index.html

# all the imports
import sqlite3
from contextlib import closing

from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash, Blueprint

# configuration
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.wsgi import WSGIContainer

DATABASE = '/Users/liuche/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()

@app.route('/')
def show_entries():
    #sqlite3 ./flaskr.db "select * from entries";
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

#蓝图,http://localhost:8080/simple_page/
simple_page = Blueprint('simple_page', __name__,template_folder='templates')
@simple_page.route('/', defaults={'page': 'index'})
@simple_page.route('/<page>/')
def show(page):
    return "Blueprint Test %s " % page
#蓝图注册在app中
app.register_blueprint(simple_page)

if __name__ == '__main__':
    # init_db()
    # app.run(port=8080)
    #tornado WSGI 容器
    http_server = HTTPServer(WSGIContainer(app))
    #flask默认的端口,可任意修改
    http_server.listen(8080)
    IOLoop.instance().start()

