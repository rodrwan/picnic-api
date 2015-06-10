#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from os import environ as env
from sys import argv

import bottle
from bottle import default_app, request, route, response, get, view

bottle.debug(True)

@get('/')
@view('views/index')
def index():
    response.content_type = 'text/html; charset=utf-8'
    title = 'Home'

    return dict(title=title)

@get('/api')
@view('views/api_template')
def api_doc():
    response.content_type = 'text/html; charset=utf-8'
    title = 'API Doc'

    return dict(title=title)

@get('/api/users')
def users():
    response.content_type = 'application/json; charset=utf-8'
    return {
        'status': 'success',
        'users': []
    }

@get('/api/categories')
def users():
    response.content_type = 'application/json; charset=utf-8'
    return {
        'status': 'success',
        'users': []
    }

bottle.run(host='0.0.0.0', port=argv[1])
