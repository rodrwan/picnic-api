#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__= 'Rodrigo Fuenzalida'
__version__= '1.0'
__license__ = 'MIT'
__email__ = 'rf@finciero.com'

import os
from os import environ as env
from sys import argv
import json

import bottle
from bottle import default_app, request, route, response, get, post, view
import bottle_pgsql
import psycopg2
import urlparse

pgdb   = 'picnic'
pguser = os.environ.get('PG_USER')
pghost = os.environ.get('PG_HOST')
connectionData  = pgdb, pguser, pghost
connectionStr = "dbname='{0[0]}' user='{0[1]}' host='{0[2]}'"
connectionQuery = connectionStr.format(connectionData)
try:
    urlparse.uses_netloc.append("postgres")
    url = urlparse.urlparse(os.getenv("DATABASE_URL", 'no db url'))
    conn = psycopg2.connect(
      database=url.path[1:],
      user=url.username,
      password=url.password,
      host=url.hostname,
      port=url.port
    )
except:
    conn = psycopg2.connect(connectionQuery)

# plugin = bottle_pgsql.Plugin(connectionQuery)
bottle.debug(True)
# bottle.install(plugin)

class EnableCors(object):
    name = 'enable_cors'
    api = 2

    def apply(self, fn, context):
        def _enable_cors(*args, **kwargs):
            # set CORS headers
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

            if bottle.request.method != 'OPTIONS':
                # actual request; reply with the actual response
                return fn(*args, **kwargs)

        return _enable_cors

# the decorator
def enable_cors(fn):
    def _enable_cors(*args, **kwargs):
        # set CORS headers
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

        if bottle.request.method != 'OPTIONS':
            # actual request; reply with the actual response
            return fn(*args, **kwargs)

    return _enable_cors

# bottle.install(EnableCors())

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

@route('/api/documentaries', methods=['GET'])
@enable_cors
def documentaries():
    response.content_type = 'application/json; charset=utf-8'
    db = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql = "SELECT * FROM documentaries;"
    db.execute(sql)
    rows = db.fetchall()
    db.close()

    data = []
    for row in rows:
        category = {}
        for key,value in row.items():
            category[key] = value
        data.append(category)
    if data:
        return {
            'status': 'success',
            'documentaries': data
        }
    else:
        return {
            'status': 'success',
            'users': []
        }

@post('/api/users')
def users_post():
    response.content_type = 'application/json; charset=utf-8'
    res = request.json

    return {
        'status': 'success',
        'data': res['data']
    }

@route('/api/categories', methods=['GET'])
@enable_cors
def categories():
    response.content_type = 'application/json; charset=utf-8'
    db = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql = "SELECT * FROM categories;"
    db.execute(sql)
    rows = db.fetchall()
    db.close()

    data = []
    for row in rows:
        category = {}
        for key,value in row.items():
            category[key] = value
        data.append(category)
    if data:
        return {
            'status': 'success',
            'categories': data
        }
    else:
        return {
            'status': 'success',
            'users': []
        }

@route('/api/categories/<category>', methods=['GET'])
@enable_cors
def category(category):
    response.content_type = 'application/json; charset=utf-8'
    db = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql = "SELECT * FROM category_topics ct WHERE ct.category_id = '" + category + "';"
    db.execute(sql)
    rows = db.fetchall()
    db.close()

    data = {}
    for row in rows:
        data[row['category_id']] = {}
        data[row['category_id']]['sub_title'] = row['sub_category_name']
        data[row['category_id']]['topics'] = []

    for row in rows:
        topic = {
            'id': row['id'],
            'thumbnail': row['thumbnail'],
            'title': row['title'],
            'subTitle': row['sub_title'],
            'brief': row['brief'],
            'time': row['total_time']
        }
        data[row['category_id']]['topics'].append(topic)

    if data:
        return {
            'status': 'success',
            'topics': data
        }
    else:
        return {
            'status': 'success',
            'users': []
        }

@get('/api/categories/<category>/topic/<id>')
@enable_cors
def topic(category, id):
    response.content_type = 'application/json; charset=utf-8'
    db = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql = "SELECT * FROM content WHERE id = '" + id + "';"
    db.execute(sql)
    rows = db.fetchone()

    data = {}
    for key,value in rows.items():
        data[key] = value

    if data:
        return {
            'status': 'success',
            'topic': data
        }
    else:
        return {
            'status': 'success',
            'users': []
        }

bottle.error(404)
def error404(error):
    return json.dumps({
      'statusCode': 404,
      'status': 'error',
      'message': 'Not Found'
    })

bottle.error(500)
def error500(error):
    return json.dumps({
      'statusCode': 500,
      'status': 'error',
      'message': 'Internal Server Error, our fat cat did something wrong'
    })

bottle.run(host='0.0.0.0', port=argv[1])
