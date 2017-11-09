# -*- coding:utf-8 -*-
import time
from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = 'some_secret'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or \
                        request.form['password'] != 'admin':
            error = 'Invalid credentials'
        else:
            logintime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print logintime
            flash('You were successfully logged in')
            flash('login time : %s' % logintime)
            return redirect(url_for('index'))
    return render_template('flashlogin.html', error=error)

if __name__ == "__main__":
    app.run(port=8080)
