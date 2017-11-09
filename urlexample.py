# -*- coding:utf-8 -*-
import types

from flask import Flask, g, Blueprint

app = Flask(__name__)

# @app.url_defaults
# def add_language_code(endpoint, values):
#     print "add_language_code"
#     if values==None:
#         return
#     if 'lang_code' in values or not g.lang_code:
#         return
#     if app.url_map.is_endpoint_expecting(endpoint, 'lang_code'):
#         values['lang_code'] = g.lang_code
#
# @app.url_value_preprocessor
# def pull_lang_code(endpoint, values):
#     print "pull_lang_code"
#     if values==None:
#         return
#     g.lang_code = values.pop('lang_code', None)
#
# @app.route('/<lang_code>/')
# def index():
#     # g.lang_code = lang_code
#     return g.lang_code
#
# @app.route('/<lang_code>/about')
# def about():
#     # g.lang_code = lang_code
#     return g.lang_code+"about"


bp = Blueprint('frontend', __name__, url_prefix='/<bplang_code>')

@bp.url_defaults
def add_language_code(endpoint, values):
    print "add_language_code"
    values.setdefault('bplang_code', g.lang_code)

@bp.url_value_preprocessor
def pull_lang_code(endpoint, values):
    print "pull_lang_code"
    g.bplang_code = values.pop('bplang_code')

@bp.route('/')
def bpindex():
    return g.bplang_code

@bp.route('/about')
def bpabout():
    return g.bplang_code+"about"

app.register_blueprint(bp)

if __name__ == '__main__':
    app.run(port=8080)