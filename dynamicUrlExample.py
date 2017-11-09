# -*- coding:utf-8 -*-
"""
动态视图
"""

from flask import Flask
from werkzeug.utils import cached_property, import_string

import views

class LazyView(object):

    def __init__(self, import_name):
        self.__module__, self.__name__ = import_name.rsplit('.', 1)
        self.import_name = import_name

    @cached_property
    def view(self):
        return import_string(self.import_name)

    def __call__(self, *args, **kwargs):
        return self.view(*args, **kwargs)

def url(url_rule, import_name, **options):
    view = LazyView('dynamicUrlExample.' + import_name)
    app.add_url_rule(url_rule, view_func=view, **options)

app = Flask(__name__)

#method 1
#app.add_url_rule('/', view_func=views.helloWorld)
#method 2
#app.add_url_rule('/',view_func=LazyView('dynamicUrlExample.views.helloWorld'))
#method 3
url('/', 'views.helloWorld')

if __name__ == '__main__':
    app.run(port=8080)