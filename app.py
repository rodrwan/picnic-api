#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from os import environ as env
from sys import argv

import bottle
from bottle import default_app, request, route, response, get

bottle.debug(True)

@get('/')
def index():
    response.content_type = 'application/html; charset=utf-8'
    ret = 'If you need to see the API Doc go to:'
    ret += '<a href="/api">API Doc</a>'
    return ret

@get('/api')
def api_doc():
    response.content_type = 'application/html; charset=utf-8'
    ret = 'API Doc'

    return ret

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
