#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__= 'Rodrigo Fuenzalida'
__version__= '1.0'
__license__ = 'MIT'
__email__ = 'rf@finciero.com'

import psycopg2
import urlparse
import os
pgdb   = 'picnic'
pguser = os.environ.get('PG_USER')
pghost = os.environ.get('PG_HOST')
connectionData  = pgdb, pguser, pghost
connectionStr = "dbname='{0[0]}' user='{0[1]}' host='{0[2]}'"
connectionQuery = connectionStr.format(connectionData)
try:
    urlparse.uses_netloc.append("postgres")
    # url = urlparse.urlparse('postgres://nlqlebihfzfpyi:TA6U266O4fA3ktsSZhVDg7jG2b@ec2-54-83-205-164.compute-1.amazonaws.com:5432/d1ih96mbtah8j6')
    url = urlparse.urlparse(os.getenv("DATABASE_URL", 'no url')) #
    conn = psycopg2.connect(
      database=url.path[1:],
      user=url.username,
      password=url.password,
      host=url.hostname,
      port=url.port
    )
except:
    conn = psycopg2.connect(connectionQuery)

print "Create SQLite db"
c = conn.cursor()

sql = """
ALTER TABLE "category_topics" DROP CONSTRAINT category_topics_fk0;
ALTER TABLE "lectures" DROP CONSTRAINT lectures_fk0;
ALTER TABLE "content" DROP CONSTRAINT content_pk;
"""
c.execute(sql)
print "alter droped"

sql = """
DROP TABLE IF EXISTS "documentaries";
DROP TABLE IF EXISTS "categories";
DROP TABLE IF EXISTS "content";
DROP TABLE IF EXISTS "category_topics";
DROP TABLE IF EXISTS "users";
DROP TABLE IF EXISTS "lectures";
"""
c.execute(sql)
print "system clear"
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
print "doc 1"
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
print "doc 2"
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
print "doc 3"
sql = """
INSERT INTO documentaries (id, thumbnail, title, sub_title, brief, content, media, type, time) VALUES (4, 'doc4/thumbnail.png', 'Estos tíos exóticos de barcelona', 'Documentales, 1 video', 'Documental trata sobre la situación actual del diseño en Barcelona, en el que participan varios diseñadores dando su opinión y lo que esperan del futuro.', 'Creado hace algunos años como proyecto de titulo, este documental trata sobre la situación actual del diseño en Barcelona. En él, varios profesionales del diseño dan sus opiniones sobre la evolución del sector en esta ciudad y lo que esperan que ocurra en el futuro.', 'doc4', 'local', '47,25');
"""
c.execute(sql)
print "doc 4"
sql = """
INSERT INTO documentaries (id, thumbnail, title, sub_title, brief, content, media, type, time) VALUES (5, 'doc5/thumbnail.png', '¿Qué es el diseño gráfico?', 'Documentales, 1 video', 'Documental argentino en el cual profesionales del diseño gráfico tratan de explicar qué es el diseño gráfico, de el salen varias preguntas para reflexionar.', 'Documental argentino en el que catedráticos, profesionales y expertos intentan definir “diseño gráfico”. Surgen preguntas interesantes y es un documental que nos hará reflexionar.', 'doc5', 'local', '55,50');
"""
c.execute(sql)
print "doc 5"
sql = """
INSERT INTO documentaries (id, thumbnail, title, sub_title, brief, content, media, type, time) VALUES (6, 'doc6/thumbnail.png', 'No logo', 'Documentales, 1 video', 'Basado en el best-seller de Naomi Klein, trata del impacto que tienen las marcas en la sociedad.', 'Documental basado en el best-seller de Naomi Klein del mismo nombre. Trata del impacto de las marcas en la sociedad', 'doc6', 'local', '40,38');
"""
c.execute(sql)
print "doc 6"
sql = """
INSERT INTO categories (id, title, image, description)
VALUES ('history', 'Historia y Teoría', 'history.jpg', 'Descubre videos de historia del arte, acotencimientos historicos de los tiempos del diseño, y todo sobre cultura.');
"""
c.execute(sql)
print "history"
sql = """
INSERT INTO categories (id, title, image, description)
VALUES ('economy', 'Economía y Gestión', 'economy.jpg', 'Descubre videos de gestión para perfeccionar tus proyectos, videos de gestión en branding, y aprende a llevar tus proyectos de una forma correcta.');
"""
c.execute(sql)
print "economy"
sql = """
INSERT INTO category_topics (id, category_id, sub_category_id, sub_category_name, thumbnail, title, sub_title, brief, total_time)
VALUES (1, 'history', 1, 'Historia del Diseño', 'history/hist1/hist1.jpg', 'Art & craft', 'Historia del diseño, 1 video', 'Surgió en las últimas décadas del siglo XIX contra el primer estilo industrial desarrollado en Inglaterra, el estilo Victoriano.', 05.05);
"""
c.execute(sql)
print "cat 1"
sql = """
INSERT INTO category_topics (id, category_id, sub_category_id, sub_category_name, thumbnail, title, sub_title, brief, total_time)
VALUES (2, 'history', 2, 'Historia del Diseño', 'history/hist2/hist2.jpg', 'Vanguardias', 'Historia del diseño, 3 videos', 'Feuvismo conocido como Fauvismo 1904-1908, Cubismo 1907-1914, Futurismo 1909.', 13.28);
"""
c.execute(sql)
print "cat 2"
sql = """
INSERT INTO category_topics (id, category_id, sub_category_id, sub_category_name, thumbnail, title, sub_title, brief, total_time)
VALUES (3, 'history', 3, 'Historia del Diseño', 'history/hist3/hist3.jpg', 'Posguerra', 'Historia del diseño, 4 videos', 'Con el fin de la segunda guerra Mundial se consolida el diseño Industrial, en Alemania e Italia este fue un factor determinante para la reconstrucción de sus respectivos países y el refuerzo de su identidad.', 19.42);
"""
c.execute(sql)
print "cat 3"
sql = """
INSERT INTO category_topics (id, category_id, sub_category_id, sub_category_name, thumbnail, title, sub_title, brief, total_time)
VALUES (4, 'history', 4, 'Historia del Diseño', 'history/hist4/hist4.jpg', 'Posmodernismo', 'Historia del diseño, 2 videos', 'Surge un amplio numero de movimientos artísticos, culturales, literarios y filosóficos del siglo XX.', 34.70);
"""
c.execute(sql)
print "cat 4"
sql = """
INSERT INTO category_topics (id, category_id, sub_category_id, sub_category_name, thumbnail, title, sub_title, brief, total_time)
VALUES (5, 'history', 5, 'Historia del Diseño en Chile', 'history/hist5/hist5.png', 'ORÍGENES, TRADICIONES Y PRACTICAS', 'Historia del Diseño en Chile, 1 video', 'En el siglo XVIII, las Bellas Artes se separan de las prácticas artísticas con fines utilitarios, y la industrialización da paso al nacimiento de las llamadas Artes Aplicadas.', 51.01);
"""
c.execute(sql)
print "cat 5"
sql = """
INSERT INTO category_topics (id, category_id, sub_category_id, sub_category_name, thumbnail, title, sub_title, brief, total_time)
VALUES (6, 'history', 6, 'Historia del Diseño en Chile', 'history/hist6/hist6.jpg', 'VICENTE LARREA AÑOS 60', 'Historia del Diseño en Chile, 1 videos', 'Se reconoce como un muchacho inquieto, que no fue ninguna lumbrera, porque desde que tomó la primera tiza, se dio cuenta que lo suyo eran las rayas, el dibujo, el diseño.', 21.09);
"""
c.execute(sql)
print "cat 6"
sql = """
INSERT INTO category_topics (id, category_id, sub_category_id, sub_category_name, thumbnail, title, sub_title, brief, total_time)
VALUES (7, 'history', 7, 'Historia del Diseño en Chile', 'history/hist7/hist7.png', 'CARTELISMO AÑOS 70', 'Historia del Diseño en Chile, 1 videos', 'Carteles políticos del periodo de gobierno de Salvador Allende y la Unidad Popular de Chile (1971-1973).', 3.28);
"""
c.execute(sql)
print "cat 7"
sql = """
INSERT INTO category_topics (id, category_id, sub_category_id, sub_category_name, thumbnail, title, sub_title, brief, total_time)
VALUES (8, 'history', 8, 'Historia del Diseño en Chile', 'history/hist8/hist8.png', 'DA DISEÑADORES ASOCIADOS 1981', 'Historia del Diseño en Chile, 1 videos', 'Se funda la primera empresa de diseño "Diseñadores Asociados"', 2.16);
"""
c.execute(sql)
print "cat 8"
sql = """
INSERT INTO category_topics (id, category_id, sub_category_id, sub_category_name, thumbnail, title, sub_title, brief, total_time)
VALUES (9, 'history', 9, 'Historia del Diseño en Chile', 'history/hist9/hist9.png', 'COLEGIO DE DISEÑADORES 1985', 'Historia del Diseño en Chile, 1 videos', 'Creación del Colegio de Diseñadores Profesionales de Chile.', 0.35);
"""
c.execute(sql)
print "cat 9"
sql = """
INSERT INTO category_topics (id, category_id, sub_category_id, sub_category_name, thumbnail, title, sub_title, brief, total_time)
VALUES (10, 'history', 10, 'Historia del Diseño en Chile', 'history/hist10/hist10.png', 'VICENTE LARREA DISEÑO SOCIAL V/S DISEÑO COMERCIAL', 'Historia del Diseño en Chile, 2 videos', 'El destacado diseñador habla sobre el diseño, la impresión y la evolución de estos.', 3.14);
"""
c.execute(sql)
print "cat 10"
sql = """
INSERT INTO category_topics (id, category_id, sub_category_id, sub_category_name, thumbnail, title, sub_title, brief, total_time)
VALUES (11, 'history', 11, 'Historia del Diseño en Chile', 'history/hist11/hist11.png', 'DISEÑO EDITORIAL, PRISMA TV ', 'Historia del Diseño en Chile, 1 videos', 'Entrevista a Revista Paula, The Clinic, Joia magazine,  portafolio de estudio gráfico Lamano.', 24.43);
"""
c.execute(sql)
print "cat 11"
sql = """
INSERT INTO category_topics (id, category_id, sub_category_id, sub_category_name, thumbnail, title, sub_title, brief, total_time)
VALUES (12, 'history', 12, 'Historia del Diseño en Chile', 'history/hist12/hist12.png', 'NUEVOS MEDIOS, PRISMA TV', 'Historia del Diseño en Chile, 1 videos', 'Entrevista a DelightLab, Sebastián Skoknic y Oktopus, portafolio de Ayerviernes.', 25.35);
"""
c.execute(sql)
print "cat 12"
sql = """
INSERT INTO category_topics (id, category_id, sub_category_id, sub_category_name, thumbnail, title, sub_title, brief, total_time)
VALUES (13, 'history', 13, 'Historia del Diseño en Chile', 'history/hist13/hist13.png', 'TIPOGRAFÍA, PRISMA TV', 'Historia del Diseño en Chile, 1 videos', 'Entrevista a Latinotype, Francisco Gálvez, Roberto Osses y Zelén Vargas, portafolio de Leyenda.', 25.47);
"""
c.execute(sql)
print "cat 13"
sql = """
INSERT INTO category_topics (id, category_id, sub_category_id, sub_category_name, thumbnail, title, sub_title, brief, total_time)
VALUES (14, 'history', 14, 'Historia del Diseño en Chile', 'history/hist14/hist14.png', 'STREET ART, PRISMA TV', 'Historia del Diseño en Chile, 1 videos', 'Entrevistados Raverlab, Galería Bomb y Mono González, portafolio de Carburadores.', 29.20);
"""
c.execute(sql)
print "cat 14"


sql =  """
INSERT INTO content (id, category_topic_id, content_title, content, media, type, time)
VALUES (1, 1, 'Romanticismo', '<p>El movimiento Arts and Crafts (Artes y oficios) fue un movimiento artístico que surgió en Inglaterra en 1880 y se desarrolló en el Reino Unido y Estados Unidos en los últimos años del siglo XIX y comienzos del siglo XX.</p><p>El Arts & Crafts se asocia sobre todo con la figura de William Morris, artesano, impresor, diseñador, escritor, poeta, activista político y, en fin, hombre polifacético, que se ocupó de la recuperación de los artes y oficios medievales, renegando de las nacientes formas de producción en masa. Aparte de William Morris, sus principales impulsores fueron Charles Robert Ashbee, T. J. Cobden Sanderson, Walter Crane, Phoebe Anna Traquair, Herbert Tudor Buckland, Charles Rennie Mackintosh, Frank Lloyd Wright, Christopher Dresser, Edwin Lutyens, Ernest Gimson, Gustav Stickley, y los artistas del movimiento prerrafaelita.</p>', 'OV1M09Hj4DU', 'youtube', 05.05);
"""
c.execute(sql)
print "cat 15"
sql = """
INSERT INTO content (id, category_topic_id, content_title, content, media, type, time)
VALUES (2, 2, 'Feuvismo', '<p>El feuvismo, también conocido como fauvismo, en francés fauvisme, (1904-1908) fue un movimiento pictórico francés caracterizado por un empleo provocativo del color. Su nombre procede del calificativo fauve, fiera en español, dado por el crítico de arte Louis Vauxcelles al conjunto de obras presentadas en el Salón de Otoño de París de 1905. El precursor de este movimiento fue Henri Matisse y su mayor influencia en la pintura posterior se ha relacionado con la utilización libre del color.</p>', 'BwbsIRMTw3g', 'youtube', 03.55);
"""
c.execute(sql)
print "cat 16"
sql = """
INSERT INTO content (id, category_topic_id, content_title, content, media, type, time)
VALUES (3, 2, 'Cubismo', E'<p>El cubismo fue un movimiento artístico desarrollado entre 1907 y 1914, nacido en Francia y encabezado por Pablo Picasso, Georges Braque, Jean Metzinger, Albert Gleizes, Robert Delaunay y Juan Gris. Es una tendencia esencial, pues da pie al resto de las vanguardias europeas del siglo XX. No se trata de un ismo más, sino de la ruptura definitiva con la pintura tradicional.</p><p>El término cubismo fue acuñado por el crítico francés Louis Vauxcelles, el mismo que había bautizado a los fauvistas motejándolos de fauves (fieras); en el caso de Braque y sus pinturas de L\\'Estaque, Vauxcelles dijo, despectivamente, que era una pintura compuesta por «pequeños cubos». Se originó así el concepto de «cubismo». El cubismo literario es otra rama que se expresa con poesías cuya estructura forma figuras o imágenes que ejemplifican el tema, la rima es opcional y ni tienen una métrica específica ni se organizan en versos.</p>', 'Rn8UFDKUoRc', 'youtube', 05.03);
"""
c.execute(sql)
print "cat 17"
sql = """
INSERT INTO content (id, category_topic_id, content_title, content, media, type, time)
VALUES (4, 2, 'Futurismo', '<p>El futurismo surgió en Milán, Italia, impulsado por Filippo Tommaso Marinetti. Este movimiento buscaba romper con la tradición, el pasado y los signos convencionales que la historia del arte consideraba como elementos principales a la poesía, el valor, la audacia y la revolución, ya que se pregonaba el movimiento agresivo, el insomnio febril, el paso gimnástico, el salto peligroso y la bofetada irreverente. Tenía como postulados: la exaltación de lo sensual, lo nacional y guerrero, la adoración de la máquina, el retrato de la realidad en movimiento, lo objetivo de lo literario y la disposición especial de lo escrito, con el fin de darle una expresión plástica.</p><p>Rechazaba la estética tradicional e intentó ensalzar la vida contemporánea, basándose en sus dos temas dominantes: la máquina y el movimiento. Se recurría, de este modo, a cualquier medio expresivo (artes plásticas, arquitectura, urbanismo, publicidad, moda, cine, música, poesía) capaz de crear un verdadero arte de acción, con el propósito de rejuvenecer y construir un nuevo orden en el mundo.</p>', '847y5CGCqys', 'youtube', 04.30);
"""
c.execute(sql)
print "cat 18"
sql = """
INSERT INTO content (id, category_topic_id, content_title, content, media, type, time)
VALUES (5, 3, 'POST-GUERRA', '', 'ni72mNDNBV4', 'youtube', 5.51);
"""
c.execute(sql)
print "cat 19"
sql = """
INSERT INTO content (id, category_topic_id, content_title, content, media, type, time)
VALUES (6, 3, 'POST-GUERRA', '', 'X7GaJTi1ceQ', 'youtube', 1.01);
"""
c.execute(sql)
print "cat 20"
sql = """
INSERT INTO content (id, category_topic_id, content_title, content, media, type, time)
VALUES (7, 3, 'POST-GUERRA', '', '308PDQ3szaM', 'youtube', 5.48);
"""
c.execute(sql)

sql = """
INSERT INTO content (id, category_topic_id, content_title, content, media, type, time)
VALUES (8, 3, 'POST-GUERRA', '', 'V5BiVuMDtWU', 'youtube', 7.39);
"""
c.execute(sql)
print "cat 21"
sql = """
INSERT INTO content (id, category_topic_id, content_title, content, media, type, time)
VALUES (9, 4, 'POST-MODERNISMO ', '<p>Las diferentes corrientes del movimiento postmoderno aparecieron durante la segunda mitad del siglo XX. Aunque se aplica a corrientes muy diversas, todas ellas comparten la idea de que el proyecto modernista fracasó en su intento de renovación radical de las formas tradicionales del arte y la cultura, el pensamiento y la vida social.</p><p>El término posmodernidad o postmodernidad fue utilizado para designar generalmente a un amplio número de movimientos artísticos, culturales, literarios y filosóficos del siglo XX, que se extienden hasta hoy, definidos en diverso grado y manera por su oposición o superación de las tendencias de la Edad Moderna.', 'aw_QtNv_ofs', 'youtube', 8.40);
"""
c.execute(sql)
print "cat 22"
sql = """
INSERT INTO content (id, category_topic_id, content_title, content, media, type, time)
VALUES (10, 4, 'POST-MODERNISMO ', '', 'ul8avVPEGME', 'youtube', 26.30);
"""
c.execute(sql)
print "cat 23"
sql = """
INSERT INTO content (id, category_topic_id, content_title, content, media, type, time)
VALUES (11, 5, 'ORÍGENES, TRADICIONES Y PRACTICAS', '<p>En Chile, la Escuela de Artes Aplicadas de la Universidad de Chile es el antecedente previo para la fundación, a fines de los setenta, de las primeras escuelas de diseño en el país. De ahí que el Diseño gráfico, como disciplina proyectual y actividad profesional, reconozca un desarrollo de poco más de cuatro décadas. En el capítulo, referentes generacionales de todo este proceso reflexionaran en torno a aristas de índole internacional y nacional privadas de consenso: el origen diferenciado como práctica y disciplina; la conciliación entre la autoría y el funcionalismo; y el complejo distingo de una identidad visual país.</p>', 'qf6FbdhNk7g', 'youtube', 51.01);
"""
c.execute(sql)
print "cat 24"
sql = """
INSERT INTO content (id, category_topic_id, content_title, content, media, type, time)
VALUES (12, 6, 'VICENTE LARREA AÑOS 60', '<p>En 1961 ingresa a la Escuela de Artes Aplicadas de la Universidad de Chile, estudia dibujo publicitario y decoración de interiores.</p><p>En 1963 se incorpora al Departamento de Extensión Cultural de la U.de Chile, donde se dedica a la producción de material informativo para las escuelas de temporada. En 1967 ante la alta demanda del carteles, Larrea instala una oficina en la calle Huérfanos y la carátula del primer disco del grupo folcklórico Quilapayún lo hace conocido.</p>', 'SnCxI9aaL5s', 'youtube', 21.09);
"""
c.execute(sql)
print "cat 25"
sql = """
INSERT INTO content (id, category_topic_id, content_title, content, media, type, time)
VALUES (13, 7, 'CARTELISMO AÑOS 70', '<p>En 1961 ingresa a la Escuela de Artes Aplicadas de la Universidad de Chile, estudia dibujo publicitario y decoración de interiores.</p><p>En 1963 se incorpora al Departamento de Extensión Cultural de la U.de Chile, donde se dedica a la producción de material informativo para las escuelas de temporada. En 1967 ante la alta demanda del carteles, Larrea instala una oficina en la calle Huérfanos y la carátula del primer disco del grupo folcklórico Quilapayún lo hace conocido.</p>', 'SnCxI9aaL5s', 'youtube', 21.09);
"""
c.execute(sql)
print "cat 26"
sql = """
INSERT INTO content (id, category_topic_id, content_title, content, media, type, time)
VALUES (14, 8, 'VICENTE LARREA AÑOS 60', '<p>En 1981 nace la empresa  DA Diseñadores Asociados ofreciendo a sus clientes asesorías integrales y estratégicas en proyectos de imagen corporativa y comunicaciones. Hoy en día DA es un equipo joven que conversa la experiencia, seriedad y metodología durante su trayectoria, incorporando tecnología, creatividad e innovación.</p>', 'EURynRnl8L8', 'youtube', 2.16);
"""
c.execute(sql)
print "cat 27"
sql = """
INSERT INTO content (id, category_topic_id, content_title, content, media, type, time)
VALUES (15, 9, 'COLEGIO DE DISEÑADORES 1985', '<p>Nace en 1985 es el órgano encargado de promover la racionalización, desarrollo y protección de la actividad profesional del diseño en todas sus áreas en nuestro país.</p>', 'qc9pJDWYQdA', 'youtube', 0.35);
"""
c.execute(sql)
print "cat 28"
sql = """
INSERT INTO content (id, category_topic_id, content_title, content, media, type, time)
VALUES (16, 10, 'VICENTE LARREA DISEÑO SOCIAL V/S DISEÑO COMERCIAL', '<p>Vicente Larrea Fundador de Larrea Diseñadores y Larrea Impresores, nos habla sobre diseño, impresión y la evolución de estos a través del tiempo.</p>', 'jEeq98tW3pA', 'youtube', 1.59);
"""
c.execute(sql)
print "cat 29"
sql = """
INSERT INTO content (id, category_topic_id, content_title, content, media, type, time)
VALUES (17, 10, 'VICENTE LARREA DISEÑO SOCIAL V/S DISEÑO COMERCIAL', '', 'XJHEtWvsNTM', 'youtube', 1.55);
"""
c.execute(sql)
print "cat 30"
sql = """
INSERT INTO content (id, category_topic_id, content_title, content, media, type, time)
VALUES (18, 11, 'DISEÑO EDITORIAL, PRISMA TV ', '<p>Diseño Editorial especificamente de revistas como Paula, The Clinic y Joia Magazine, los cuales hablan del concepto que hay detrás, el publico objetivo al cual se dirigen, como trabajan, los cambios que han tenido en la editorial y el porque se producen estos cambios y como esta el mercado editorial en Chile.</p>', 'hist11', 'local', 24.43);
"""
c.execute(sql)
print "cat 31"
sql = """
INSERT INTO content (id, category_topic_id, content_title, content, media, type, time)
VALUES (19, 12, 'NUEVOS MEDIOS, PRISMA TV', '<p>Evolución de los medios, experiencias nuevas que transmiten y cómo están conectados entre si, como lo habitual deja de serlo y que pasa en Chile con estos nuevos medios y cómo están relacionados con el diseño gráfico.</p>', 'hist12', 'local', 25.35);
"""
c.execute(sql)
print "cat 32"
sql = """
INSERT INTO content (id, category_topic_id, content_title, content, media, type, time)
VALUES (20, 13, 'TIPOGRAFÍA, PRISMA TV ', '<p>La idea de tipografía, cuáles son los conceptos que hay detrás y de acuerdo a esto cual es la que se debería utilizar, y qué esta pasando en Chile en el ámbito tipográfico.</p>', 'hist13', 'local', 25.47);
"""
c.execute(sql)
print "cat 33"
sql = """
INSERT INTO content (id, category_topic_id, content_title, content, media, type, time)
VALUES (21, 14, 'STREET ART, PRISMA TV ', '<p>El valor de la calle, la expresión artística y cultural que posee y cómo esto esta relacionado con el diseño gráfico.</p>', 'hist14', 'local', 29.20);
"""
c.execute(sql)

print "cat 34"
sql = """
INSERT INTO category_topics (id, category_id, sub_category_id, sub_category_name, thumbnail, title, sub_title, brief, total_time)
VALUES (15, 'economy', 15, 'GESTIÓN DE PROYECTOS', 'economy/econ1/econ1.jpg', 'FUNCIONES DE ADMINISTRACIÓN DE LA EMPRESA', 'GESTIÓN DE PROYECTOS, LECTURA', 'Según Henry Fayol, toda empresa cumple seis funciones básicas.', 0);
"""
c.execute(sql)
print "cat 35"
sql = """
INSERT INTO category_topics (id, category_id, sub_category_id, sub_category_name, thumbnail, title, sub_title, brief, total_time)
VALUES (16, 'economy', 16, 'GESTIÓN DE PROYECTOS', 'economy/econ2/econ2.png', 'RECONOCER E IDENTIFICAR LAS GERENCIAS DE ÁREA', 'GESTIÓN DE PROYECTOS, 1 VIDEO', 'Organigrama, tipos de organigramas', 4.02);
"""
c.execute(sql)
print "cat 36"
sql = """
INSERT INTO category_topics (id, category_id, sub_category_id, sub_category_name, thumbnail, title, sub_title, brief, total_time)
VALUES (17, 'economy', 17, 'TIPOS DE EMPRESAS', 'economy/econ3/econ3.png', 'CONSTITUCIÓN DE UNA EMPRESA MINISTERIO DE ECONOMÍA, GOBIERNO DE CHILE', 'GESTIÓN DE PROYECTOS, 1 VIDEO', 'Funciones administrativas, finanzas, producción y rol de la organización', 6.53);
"""
c.execute(sql)
print "cat 37"
sql = """
INSERT INTO category_topics (id, category_id, sub_category_id, sub_category_name, thumbnail, title, sub_title, brief, total_time)
VALUES (18, 'economy', 18, 'TIPOS DE EMPRESAS', 'economy/econ4/econ4.jpg', 'CONOCER E IDENTIFICAR LAS EMPRESAS', 'GESTIÓN DE PROYECTOS, 1 VIDEO', 'Clasificación de las empresas según su actividad.', 13.47);
"""
c.execute(sql)
print "cat 38"
sql = """
INSERT INTO category_topics (id, category_id, sub_category_id, sub_category_name, thumbnail, title, sub_title, brief, total_time)
VALUES (19, 'economy', 19, 'TIPOS DE EMPRESAS', 'economy/econ5/econ5.png', 'MACRO Y MICRO ENTORNO', 'GESTIÓN DE PROYECTOS, 1 VIDEO', 'Entorno, micro-entorno: la empresa, proveedores, intermediarios, clientes, competencia, macro-entorno: demográfico, económico, natural, tecnológico, político y cultural.', 4.33);
"""
c.execute(sql)
print "cat 39"
sql = """
INSERT INTO category_topics (id, category_id, sub_category_id, sub_category_name, thumbnail, title, sub_title, brief, total_time)
VALUES (20, 'economy', 20, 'TIPOS DE EMPRESAS', 'economy/econ6/econ6.jpg', 'IMPORTANCIA DE LOS CANALES DE DISTRIBUCIÓN', 'GESTIÓN DE PROYECTOS, 1 VIDEO', 'Aspectos generales importantes, tamaño, valores de mercado, costos de canal.', 6.14);
"""
c.execute(sql)
print "cat 40"
sql = """
INSERT INTO category_topics (id, category_id, sub_category_id, sub_category_name, thumbnail, title, sub_title, brief, total_time)
VALUES (21, 'economy', 21, 'TIPOS DE EMPRESAS', 'economy/econ7/econ7.jpg', 'APLICANDO EL CONCEPTO DE DESIGN THINKING EN TU EMPRESA', 'GESTIÓN DE PROYECTOS, 1 VIDEO', 'La aplicación de este conceptos sirve para todo.. Sitios web, indumentaria, muebles y ¿por qué no?, para la forma en que interactuas con tu cliente.', 58.18);
"""
c.execute(sql)
print "cat 41"

sql = """
INSERT INTO category_topics (id, category_id, sub_category_id, sub_category_name, thumbnail, title, sub_title, brief, total_time)
VALUES (22, 'economy', 22, 'DESARROLLO DE EMPRENDEDORES', 'economy/econ8/econ8.png', 'IDEAS DE NEGOCIOS', 'GESTIÓN DE PROYECTOS, 9 VIDEO', 'Presentación de cortos para emprendedores.', 24.85);
"""
c.execute(sql)
print "cat 42"
sql = """
INSERT INTO category_topics (id, category_id, sub_category_id, sub_category_name, thumbnail, title, sub_title, brief, total_time)
VALUES (23, 'economy', 23, 'DESARROLLO DE EMPRENDEDORES', 'economy/econ9/econ9.jpg', 'DESCRIPCIÓN DEL NEGOCIOS', 'DESARROLLO DE EMPRENDEDORES, 2 VIDEOS, 1 ARTICULO', 'Serie de videos de ayuda para tu negocio..¿Cómo describir a tu empresa?, ¿Cuál es la misión y visión?, ¿Cómo es su estructura legal?', 29.91);
"""
c.execute(sql)
print "cat 43"
sql = """
INSERT INTO category_topics (id, category_id, sub_category_id, sub_category_name, thumbnail, title, sub_title, brief, total_time)
VALUES (24, 'economy', 24, 'DESARROLLO DE EMPRENDEDORES', 'economy/econ10/econ10.jpg', 'PRODUCTOS Y SERVICIOS', 'DESARROLLO DE EMPRENDEDORES, 4 VIDEOS, 1 ARTICULO', 'Posicionamiento de una marca, ciclo de vida, ¿cómo es el cliente y cuáles son sus necesidades?, ¿cómo patentar una idea?, procesos y procedimientos.', 31.46);
"""
c.execute(sql)
print "cat 44"
sql = """
INSERT INTO category_topics (id, category_id, sub_category_id, sub_category_name, thumbnail, title, sub_title, brief, total_time)
VALUES (25, 'economy', 25, 'DESARROLLO DE EMPRENDEDORES', 'economy/econ11/econ11.jpg', 'OPERACIONES Y ADMINISTRACIÓN', 'DESARROLLO DE EMPRENDEDORES, 3 VIDEOS', 'Aseguramiento de Calidad, Recursos humanos, Administración y estructura organizacional.', 24.73);
"""
c.execute(sql)
print "cat 45"
sql = """
INSERT INTO category_topics (id, category_id, sub_category_id, sub_category_name, thumbnail, title, sub_title, brief, total_time)
VALUES (26, 'economy', 26, 'BRANDING', 'economy/econ12/econ12.jpg', 'CONCEPTOS DE ARQUITECTURA Y CONSTRUCCIÓN DE MARCA', 'BRANDING, 3 VIDEOS', 'El significado de términos en la imagen corporativa, fases para la construcción de una marca branding y construcción persuasiva para las empresas.', 25.73);
"""
c.execute(sql)
print "cat 46"
sql = """
INSERT INTO category_topics (id, category_id, sub_category_id, sub_category_name, thumbnail, title, sub_title, brief, total_time)
VALUES (27, 'economy', 27, 'BRANDING', 'economy/econ13/econ13.png', 'EL CONSUMIDOR Y SUS VARIABLES PSICOGRAFICAS', 'BRANDING, 2 VIDEOS', 'Segmentación de mercado y Neuromarketing.', 29.45);
"""
c.execute(sql)
print "cat 47"
sql = """
INSERT INTO category_topics (id, category_id, sub_category_id, sub_category_name, thumbnail, title, sub_title, brief, total_time)
VALUES (28, 'economy', 28, 'BRANDING', 'economy/econ14/econ14.jpg', 'DISEÑO DE ADMINISTRACIÓN EN TÉRMINOS ESTRATÉGICOS', 'BRANDING, 1 VIDEO', 'Diseño de estrategias.', 4.58);
"""
c.execute(sql)
print "cat 48"
sql = """
INSERT INTO category_topics (id, category_id, sub_category_id, sub_category_name, thumbnail, title, sub_title, brief, total_time)
VALUES (29, 'economy', 29, 'BRANDING', 'economy/econ15/econ15.png', 'CICLO DE VIDA DE LAS MARCAS', 'BRANDING, 4 VIDEOS, 1 ARTICULO', 'Ciclo de vida de una marca, tipologías de consumidor, estrategias de mantención de marcas líderes, estrategias para marcas, estrategias para marcas con potencial desgastado.', 23.19);
"""
c.execute(sql)
print "cat 49"
conn.commit()
print "commit"
c.close()


print "finished"
