import os.path as Path
import sqlite3

SQL_SELECT_ALL  = '''
	SELECT
		id, created, crashed, pts, photo
	FROM
		auto
'''

SQL_SELECT_DATE = SQL_SELECT_ALL + "  WHERE created BETWEEN ? AND ? or crashed BETWEEN ? AND ? "

SQL_INSERT_AUTO = '''
	INSERT INTO auto(
	id,
	created,
	crashed,
	pts,
	photo
	)
	VALUES(?,?,?,?,?)
'''

def dict_factory(cursor, row):
	d = {}

	for idx, col in enumerate(cursor.description):
		d[col[0]] = row[idx]

	return d


def connect(db_name=None):
	"""Устанавливает соединение с бд"""
	if db_name is None:
		db_name = ":Memory:"
	conn = sqlite3.connect(db_name)
	conn.row_factory = dict_factory

	return conn


def initialize (conn, creation_script=None):
	""" инициализирует структуру бд"""
	if creation_script is None:
		   # file путь до текущего файла dirname родительский каталог
		creation_script = Path.join(Path.dirname(__file__),'resourses',  'schema.sql')
	with conn, open(creation_script) as f:
		conn.execute(f.read())


def add(conn, id, created, crashed, pts, photo):
	""" Добавляет  Авто в БД"""
	if not  id:
		raise RuntimeError ('id can not be empty.')
	with conn:
		cursor = conn.execute(SQL_INSERT_AUTO,( id, created, crashed, pts, photo))


def find_date(conn, first_date, second_date):
	with conn:
		cursor = conn.execute(SQL_SELECT_DATE,(first_date, second_date, first_date, second_date))
	return cursor.fetchall()
