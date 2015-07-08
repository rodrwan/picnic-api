#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Rodrigo Fuenzalida'
__version__ = '1.0'
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
import tokenlib

pgdb = 'picnic'
pguser = os.environ.get('PG_USER')
pghost = os.environ.get('PG_HOST')
connectionData = pgdb, pguser, pghost
connectionStr = "dbname='{0[0]}' user='{0[1]}' host='{0[2]}'"
connectionQuery = connectionStr.format(connectionData)
try:
    urlparse.uses_netloc.append("postgres")
    # url = urlparse.urlparse('postgres://nlqlebihfzfpyi:TA6U266O4fA3ktsSZhVD
    # g7jG2b@ec2-54-83-205-164.compute-1.amazonaws.com:5432/d1ih96mbtah8j6')
    url = urlparse.urlparse(os.getenv("DATABASE_URL", 'no url'))
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
            response.headers['Access-Control-Allow-Methods'] = \
                'GET, POST, PUT, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = \
                'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

            if bottle.request.method != 'OPTIONS':
                # actual request; reply with the actual response
                return fn(*args, **kwargs)

        return _enable_cors


# the decorator
def enable_cors(fn):
    def _enable_cors(*args, **kwargs):
        # set CORS headers
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = \
            'GET, POST, PUT, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = \
            'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

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
        for key, value in row.items():
            category[key] = value
        data.append(category)
    if data:
        return json.dumps(data)
    else:
        return json.dumps([])


@get('/api/users')
@enable_cors
def users():
    response.content_type = 'application/json; charset=utf-8'
    db = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql = "SELECT * FROM users;"
    db.execute(sql)
    rows = db.fetchall()
    db.close()

    if rows:
        return {
            'status': 'success',
            'data': rows
        }
    else:
        return {
            'status': 'success',
            'users': []
        }


@post('/api/user/create')
@enable_cors
def users_create():
    response.content_type = 'application/json; charset=utf-8'
    res = {
        'username': request.forms.get('username'),
        'password': request.forms.get('password'),
        'email': request.forms.get('email')
    }

    db = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    secret_token = tokenlib.make_token(res, secret="picoteo grafico")
    response.status = 200
    sql = "INSERT INTO users (username, email, password, session_token) "
    sql += "VALUES ('%s', '%s', '%s', '%s')" % (res['username'], res['email'],
                                                res['password'], secret_token)
    db.execute(sql)
    conn.commit()
    db.close()

    return {
        'status': 'success',
        'data': {
            'message': 'user created',
            'session_token': secret_token
        }
    }


@post('/api/user/session')
@enable_cors
def users_post():
    response.content_type = 'application/json; charset=utf-8'
    res = {
        'password': request.forms.get('password'),
        'email': request.forms.get('email')
    }
    db = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    response.status = 202
    sql = "SELECT username, session_token FROM users WHERE email = '%s'"
    sql += " and password = '%s'" % (res['email'], res['password'])
    db.execute(sql)
    rows = db.fetchone()
    print rows
    db.close()

    if rows:
        response.status = 202
        return {
            'status': 'success',
            'data': {
                'session_token': rows['session_token'],
                'username': rows['username']
            }
        }
    else:
        response.status = 401
        return {
            'status': 'success',
            'data': {
                'message': 'session over'
            }
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
        for key, value in row.items():
            category[key] = value
        data.append(category)

    if data:
        return json.dumps(data)
    else:
        return []


@route('/api/categories/<category>', methods=['GET'])
@enable_cors
def category(category):
    response.content_type = 'application/json; charset=utf-8'
    db = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql = "SELECT category_id, sub_category_name FROM category_topics ct "
    sql += "WHERE ct.category_id = '" + category + "' GROUP BY category_id, "
    sql += "sub_category_name;"
    db.execute(sql)
    rows = db.fetchall()

    data = []
    for row in rows:
        sub_topic = {}

        sub_topic['subTitle'] = row['sub_category_name']
        sub_topic['topics'] = []

        sql = "SELECT * FROM category_topics ct WHERE ct.category_id = '" + \
            category + "' and ct.sub_category_name = '" + \
            row['sub_category_name'] + "';"

        db.execute(sql)
        rows2 = db.fetchall()
        for row2 in rows2:
            topic = {
                'id': row2['id'],
                'thumbnail': row2['thumbnail'],
                'title': row2['title'],
                'subTitle': row2['sub_title'],
                'brief': row2['brief'],
                'time': row2['total_time']
            }

            sub_topic['topics'].append(topic)

        data.append(sub_topic)

    db.close()

    if data:
        return json.dumps(data)
    else:
        return json.dumps([])


@get('/api/categories/<category>/topic/<id>')
@enable_cors
def topic(category, id):
    response.content_type = 'application/json; charset=utf-8'
    db = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql = "SELECT * FROM category_topics ct INNER JOIN content c on "
    sql += "ct.id = c.category_topic_id WHERE c.category_topic_id ='" + \
        id + "';"
    db.execute(sql)
    rows = db.fetchall()

    topic = []
    for row in rows:
        data = {}
        data['meta'] = {}
        for key, value in row.items():
            if (key == 'title'):
                data['meta']['title'] = value
            elif (key == 'sub_title'):
                data['meta']['sub_title'] = value
            elif (key == 'thumbnail'):
                data['meta']['thumbnail'] = value
            else:
                data[key] = value
        topic.append(data)

    if topic:
        return json.dumps(topic)
    else:
        return json.dumps([])
    # topic = []
    # for row in rows:
    #     topic = {}
    #     for key, value in row.items():
    #         topic[key] = value
    #     data.append(topic)
    #
    # meta = {
    #     'title': data[0]['title'],
    #     'sub_title': data[0]['sub_title'],
    #     'thumbnail': data[0]['thumbnail']
    # }
    # if data:
    #     return json.dumps([
    #         'meta': meta,
    #         'topic': data
    #     ])
    # else:
    #     return json.dumps([
    #         'topic': [],
    #         'meta': []
    #     ])


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
