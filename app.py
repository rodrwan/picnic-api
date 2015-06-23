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
    url = urlparse.urlparse('') # 'postgres://nlqlebihfzfpyi:TA6U266O4fA3ktsSZhVDg7jG2b@ec2-54-83-205-164.compute-1.amazonaws.com:5432/d1ih96mbtah8j6'
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

def create_db():
    print "Create SQLite db"
    c = conn.cursor()

    sql = """
    CREATE TABLE "documentaries" (
    "id" integer NOT NULL,
    "thumbnail" TEXT NOT NULL,
    "title" TEXT NOT NULL,
    "sub_title" TEXT NOT NULL,
    "brief" TEXT NOT NULL,
    "content" TEXT NOT NULL,
    "media" TEXT NOT NULL,
    "type" TEXT NOT NULL,
    "time" TEXT NOT NULL,
    CONSTRAINT documentaries_pk PRIMARY KEY (id)
    ) WITH (
    OIDS=FALSE
    );
    """
    c.execute(sql)

    sql = """
    CREATE TABLE "categories" (
    "id" TEXT NOT NULL,
    "title" TEXT NOT NULL,
    "image" TEXT NOT NULL,
    "description" TEXT NOT NULL,
    CONSTRAINT categories_pk PRIMARY KEY (id)
    ) WITH (
    OIDS=FALSE
    );
    """
    c.execute(sql)

    sql = """
    CREATE TABLE "category_topics" (
    "id" integer NOT NULL,
    "category_id" TEXT NOT NULL,
    "sub_category_id" integer NOT NULL,
    "sub_category_name" TEXT NOT NULL,
    "thumbnail" TEXT NOT NULL,
    "title" TEXT NOT NULL,
    "sub_title" TEXT NOT NULL,
    "brief" TEXT NOT NULL,
    "total_time" REAL NOT NULL,
    CONSTRAINT category_topics_pk PRIMARY KEY (id)
    ) WITH (
    OIDS=FALSE
    );
    """
    c.execute(sql)

    sql = """
    ALTER TABLE "category_topics" ADD CONSTRAINT category_topics_fk0 FOREIGN KEY (category_id) REFERENCES categories(id);
    """
    c.execute(sql)

    sql = """
    CREATE TABLE "users" (
    "id" integer NOT NULL,
    "username" VARCHAR(255) NOT NULL,
    "email" VARCHAR(255) NOT NULL,
    "password" VARCHAR(255) NOT NULL,
    "session_token" VARCHAR(255) NOT NULL,
    CONSTRAINT users_pk PRIMARY KEY (id)
    ) WITH (
    OIDS=FALSE
    );
    """
    c.execute(sql)

    sql = """
    CREATE TABLE "lectures" (
    "id" integer NOT NULL,
    "user_id" integer NOT NULL,
    "section" VARCHAR(255) NOT NULL,
    "section_id" integer NOT NULL,
    CONSTRAINT lectures_pk PRIMARY KEY (id)
    ) WITH (
    OIDS=FALSE
    );
    """
    c.execute(sql)

    sql = """
    ALTER TABLE "lectures" ADD CONSTRAINT lectures_fk0 FOREIGN KEY (user_id) REFERENCES users(id);
    """
    c.execute(sql)

    sql = """
    CREATE TABLE "content" (
    "id" integer NOT NULL,
    "category_topic_id" integer NOT NULL,
    "content_title" TEXT NOT NULL,
    "content" TEXT NOT NULL,
    "media" TEXT  NOT NULL,
    "type" TEXT NOT NULL,
    "time" REAL NOT NULL,
    CONSTRAINT content_pk PRIMARY KEY (id)
    ) WITH (
    OIDS=FALSE
    );
    """
    c.execute(sql)

    sql = """
    ALTER TABLE "content" ADD CONSTRAINT content_fk0 FOREIGN KEY (category_topic_id) REFERENCES category_topics(id);
    """
    c.execute(sql)

    sql = """
    INSERT INTO documentaries (id, thumbnail, title, sub_title, brief, content, media, type, time) VALUES (1,
    'doc1/thumbnail.png',
    'Como steve jobs cambio el mundo',
    'Documentales, 1 video',
    'Historias y filosofía y logos del creador de la marca Apple.',
    'En este documental se repasa la vida, la filosofía y los logros de Steve Jobs creando una de las compañias más rentables, Apple.',
    '1Bhmz0g9CsQ', 'youtube', '43,08');
    """
    c.execute(sql)

    sql = """
    INSERT INTO documentaries (id, thumbnail, title, sub_title, brief, content, media, type, time) VALUES (2,
    'doc2/thumbnail.png',
    'Helvética',
    'Documentales, 1 video',
    'Documental sobre el diseño gráfico, la tipografía y en general sobre la cultura visual, centrado en la tipografía Helvética.',
    'Documental sobre el diseño gráfico, la tipografía y en general sobre la cultura visual. La película se centra en la popular fuente tipográfica Helvética, que en el año 2007 hizo su 50 aniversario, e incluye entrevistas con los mejores nombres del mundo del diseño como Erik Spiekermann, Matthew Carter, Massino Vignelli, Wim Crouwel,, Hernmann Zapf, Neville Brody, Stefan Sagmeister. Con motivo del 50 aniversario de esta tipografía, Gary Hustwit ha dirigido y producido una película documental que explora el uso de la tipografía en los espacios urbanos y aporta la reflexiones de renombramientos diseñadores acerca de su trabajo, el proceso creativo y las elecciones estéticas detrás de su uso.',
    'doc2',
    'local',
    '90,42');
    """
    c.execute(sql)

    sql = """
    INSERT INTO documentaries (id, thumbnail, title, sub_title, brief, content, media, type, time) VALUES (3,
    'doc3/thumbnail.png',
    'Objectified',
    'Documentales, 1 video',
    'Documental acerca del diseño industrial y la compleja relación entre los objetos manufacturados y las personas que los diseñan.',
    'Documental sobre el diseño industrial. En él se examinan los objetos y el proceso creativo de quien los diseña: desde los cepillos de dientes hasta los gadgets más sofisticados.',
    'oqPGscXtTg8',
    'youtube',
    '75,41');
    """
    c.execute(sql)

    sql = """
    INSERT INTO documentaries (id, thumbnail, title, sub_title, brief, content, media, type, time) VALUES (4, 'doc4/thumbnail.png', 'Estos tíos exóticos de barcelona', 'Documentales, 1 video', 'Documental trata sobre la situación actual del diseño en Barcelona, en el que participan varios diseñadores dando su opinión y lo que esperan del futuro.', 'Creado hace algunos años como proyecto de titulo, este documental trata sobre la situación actual del diseño en Barcelona. En él, varios profesionales del diseño dan sus opiniones sobre la evolución del sector en esta ciudad y lo que esperan que ocurra en el futuro.', 'doc4', 'local', '47,25');
    """
    c.execute(sql)
    sql = """
    INSERT INTO documentaries (id, thumbnail, title, sub_title, brief, content, media, type, time) VALUES (5, 'doc5/thumbnail.png', '¿Qué es el diseño gráfico?', 'Documentales, 1 video', 'Documental argentino en el cual profesionales del diseño gráfico tratan de explicar qué es el diseño gráfico, de el salen varias preguntas para reflexionar.', 'Documental argentino en el que catedráticos, profesionales y expertos intentan definir “diseño gráfico”. Surgen preguntas interesantes y es un documental que nos hará reflexionar.', 'doc5', 'local', '55,50');
    """
    c.execute(sql)

    sql = """
    INSERT INTO documentaries (id, thumbnail, title, sub_title, brief, content, media, type, time) VALUES (6, 'doc6/thumbnail.png', 'No logo', 'Documentales, 1 video', 'Basado en el best-seller de Naomi Klein, trata del impacto que tienen las marcas en la sociedad.', 'Documental basado en el best-seller de Naomi Klein del mismo nombre. Trata del impacto de las marcas en la sociedad', 'doc6', 'local', '40,38');
    """
    c.execute(sql)

    sql = """
    INSERT INTO categories (id, title, image, description)
    VALUES ('history', 'Historia y Teoría', 'history.jpg', 'Descubre videos de historia del arte, acotencimientos historicos de los tiempos del diseño, y todo sobre cultura.');
    """
    c.execute(sql)

    sql = """
    INSERT INTO categories (id, title, image, description)
    VALUES ('economy', 'Economía y Gestión', 'economy.jpg', 'Descubre videos de gestión para perfeccionar tus proyectos, videos de gestión en branding, y aprende a llevar tus proyectos de una forma correcta.');
    """
    c.execute(sql)

    sql = """
    INSERT INTO category_topics (id, category_id, sub_category_id, sub_category_name, thumbnail, title, sub_title, brief, total_time)
    VALUES (1, 'history', 1, 'Historia del Diseño', 'history/hist1/hist1.jpg', 'Art & craft', 'Historia del diseño, 1 video', 'Breve descripción del tema.', 05.05);
    """
    c.execute(sql)

    sql = """
    INSERT INTO category_topics (id, category_id, sub_category_id, sub_category_name, thumbnail, title, sub_title, brief, total_time)
    VALUES (2, 'history', 2, 'Historia del Diseño', 'history/hist2/hist2.jpg', 'Vanguardias', 'Historia del diseño, 6 videos', 'Breve descripción del tema.', 62.01);
    """
    c.execute(sql)

    # sql = """
    # INSERT INTO category_topics (id, category_id, sub_category_id, sub_category_name, thumbnail, title, sub_title, brief, total_time)
    # VALUES (3, 'history', 3, 'Historia del Diseño', 'history/hist3/hist3.jpg', 'Posguerra', 'Historia del diseño, 4 videos', 'Breve descripción del tema.');
    # """
    # c.execute(sql)

    # sql = """
    # INSERT INTO category_topics (id, category_id, sub_category_id, sub_category_name, thumbnail, title, sub_title, brief, total_time)
    # VALUES (4, 'history', 4, 'Historia del Diseño', 'history/hist4/hist4.jpg', 'Posmodernismo', 'Historia del diseño, 2 videos', 'Breve descripción del tema.');
    # """
    # c.execute(sql)

    sql =  """
    INSERT INTO content (id, category_topic_id, content_title, content, media, type, time)
    VALUES (1, 1, 'Romanticismo', '<p>El movimiento Arts and Crafts (Artes y oficios) fue un movimiento artístico que surgió en Inglaterra en 1880 y se desarrolló en el Reino Unido y Estados Unidos en los últimos años del siglo XIX y comienzos del siglo XX.</p><p>El Arts & Crafts se asocia sobre todo con la figura de William Morris, artesano, impresor, diseñador, escritor, poeta, activista político y, en fin, hombre polifacético, que se ocupó de la recuperación de los artes y oficios medievales, renegando de las nacientes formas de producción en masa. Aparte de William Morris, sus principales impulsores fueron Charles Robert Ashbee, T. J. Cobden Sanderson, Walter Crane, Phoebe Anna Traquair, Herbert Tudor Buckland, Charles Rennie Mackintosh, Frank Lloyd Wright, Christopher Dresser, Edwin Lutyens, Ernest Gimson, Gustav Stickley, y los artistas del movimiento prerrafaelita.</p>', 'OV1M09Hj4DU', 'youtube', 05.05);
    """
    c.execute(sql)

    sql = """
    INSERT INTO content (id, category_topic_id, content_title, content, media, type, time)
    VALUES (2, 2, 'Feuvismo', '<p>El fovismo, también conocido como fauvismo, en francés fauvisme, (1904-1908) fue un movimiento pictórico francés caracterizado por un empleo provocativo del color. Su nombre procede del calificativo fauve, fiera en español, dado por el crítico de arte Louis Vauxcelles al conjunto de obras presentadas en el Salón de Otoño de París de 1905. El precursor de este movimiento fue Henri Matisse y su mayor influencia en la pintura posterior se ha relacionado con la utilización libre del color.</p>', 'BwbsIRMTw3g', 'youtube', 03.55);
    """
    c.execute(sql)

    sql = """
    INSERT INTO content (id, category_topic_id, content_title, content, media, type, time)
    VALUES (3, 2, 'Cubismo', E'<p>El cubismo fue un movimiento artístico desarrollado entre 1907 y 1914, nacido en Francia y encabezado por Pablo Picasso, Georges Braque, Jean Metzinger, Albert Gleizes, Robert Delaunay y Juan Gris. Es una tendencia esencial, pues da pie al resto de las vanguardias europeas del siglo XX. No se trata de un ismo más, sino de la ruptura definitiva con la pintura tradicional.</p><p>El término cubismo fue acuñado por el crítico francés Louis Vauxcelles, el mismo que había bautizado a los fauvistas motejándolos de fauves (fieras); en el caso de Braque y sus pinturas de L\\'Estaque, Vauxcelles dijo, despectivamente, que era una pintura compuesta por «pequeños cubos». Se originó así el concepto de «cubismo». El cubismo literario es otra rama que se expresa con poesías cuya estructura forma figuras o imágenes que ejemplifican el tema, la rima es opcional y ni tienen una métrica específica ni se organizan en versos.</p>', 'Rn8UFDKUoRc', 'youtube', 05.03);
    """
    c.execute(sql)

    sql = """
    INSERT INTO content (id, category_topic_id, content_title, content, media, type, time)
    VALUES (4, 2, 'Futurismo', '<p>El futurismo surgió en Milán, Italia, impulsado por Filippo Tommaso Marinetti. Este movimiento buscaba romper con la tradición, el pasado y los signos convencionales que la historia del arte consideraba como elementos principales a la poesía, el valor, la audacia y la revolución, ya que se pregonaba el movimiento agresivo, el insomnio febril, el paso gimnástico, el salto peligroso y la bofetada irreverente. Tenía como postulados: la exaltación de lo sensual, lo nacional y guerrero, la adoración de la máquina, el retrato de la realidad en movimiento, lo objetivo de lo literario y la disposición especial de lo escrito, con el fin de darle una expresión plástica.</p><p>Rechazaba la estética tradicional e intentó ensalzar la vida contemporánea, basándose en sus dos temas dominantes: la máquina y el movimiento. Se recurría, de este modo, a cualquier medio expresivo (artes plásticas, arquitectura, urbanismo, publicidad, moda, cine, música, poesía) capaz de crear un verdadero arte de acción, con el propósito de rejuvenecer y construir un nuevo orden en el mundo.</p>', '847y5CGCqys', 'youtube', 04.30);
    """
    c.execute(sql)

    sql = """
    INSERT INTO content (id, category_topic_id, content_title, content, media, type, time)
    VALUES (5, 2, 'Bauhaus', '<p>Walter Adolph Georg Gropius, fundador de la Bauhaus, nació en Berlín el 18 de mayo de 1883. Fue hijo y nieto de arquitectos, estudió arquitectura en Múnich y en Berlín. Uno de los principales ideales de Gropius era representado mediante la siguiente frase: "La forma sigue a la función". Pues él buscaba la unión entre el uso y la estética.</p><p>Su trayectoria es una circunstancia que hay que considerar determinante para la orientación ideológica de Gropius, pues el joven Walter Gropius, procedente de la burguesía inteligente, trabajó en Múnich, de 1907 a 1910, con Peter Behrens, el primer arquitecto contratado por una gran empresa industrial como responsable artístico. A partir de entonces, Gropius siempre planteó el problema de la edificación en relación con el sistema industrial y con la producción en serie. Llegando incluso hasta el extremo de considerar el edificio como un producto directo de la industria y fundando así en 1943, junto con Konrad Waschsmann, una empresa de edificaciones prefabricadas.</p><p>La fábrica Fagus, de arquitectura revolucionaria, le dio en 1911 una fama que confirmó en Bolonia, en 1914, al construir para la exposición del Werkbund un palacio para oficinas de atrevida concepción estructural, estética y técnica. La guerra interrumpió su actividad de constructor, reclamado al frente. Pero durante aquellos años fue madurando en su ánimo la conciencia de que tenía un deber humano muy elevado que cumplir: la arquitectura había de desempeñar un papel en el problema social que la posguerra plantearía con toda gravedad; y este problema social había de fundirse con la estética.</p>', 'sriGH51vWTo', 'youtube', 49.13);
    """
    conn.commit()
    c.close()

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
    sql = "SELECT * FROM category_topics ct INNER JOIN content c on ct.id = c.category_topic_id WHERE c.category_topic_id ='" + id + "';"
    db.execute(sql)
    rows = db.fetchall()

    data = []
    for row in rows:
        topic = {}
        for key,value in row.items():
            topic[key] = value
        data.append(topic)

    meta = {
        'title': data[0]['title'],
        'sub_title': data[0]['sub_title'],
        'thumbnail': data[0]['thumbnail']
    }
    if data:
        return {
            'status': 'success',
            'meta': meta,
            'topics': data
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

# create_db()
# print "db created"
bottle.run(host='0.0.0.0', port=argv[1])
