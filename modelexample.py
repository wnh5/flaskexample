# -*- coding:utf-8 -*-
from flask import Flask

from database import db_session, init_db
from models import User

app = Flask(__name__)

@app.route("/add/")
def adduser():
    u = User('admin', 'admin@localhost')
    db_session.add(u)
    db_session.commit()
    return "success"

@app.route("/query/<user>/")
def queryuser(user):
    u = User.query.filter(User.name == user).first()
    return u.name

@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    init_db()
    app.run(port=8080)