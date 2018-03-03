# -*- coding: utf-8 -*-

from roommates import app

from flask import session, redirect, url_for, g, render_template
from functools import wraps

from contextlib import closing # for database-things

import sqlite3

@app.template_filter()
def reverse(s):
	return s[::-1]


@app.template_filter()
def link_wiki(content):
	while '==' in content:
		parts = content.split('==', 2)

		parts[1] = '<a href="' + url_for( 'wiki_page', key=parts[1] ) + '">' + parts[1].replace('_', ' ') + '</a>'
		content = ''.join(parts)
	return content


@app.template_filter()
def currency(content):
	string = str(round(content, 2))

	numbers = string.split('.')

	print(numbers)

	if len(numbers) == 1 or numbers[1] == '0':
		return numbers[0]
	else:
		if len(str(numbers[1])) == 1:
			return numbers[0] + '.' + numbers[1] + '0'
		else:
			return numbers[0] + '.' + numbers[1]


def login_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if not session.get('id'):
			return redirect(url_for('login'))
		return f(*args, **kwargs)
	return decorated_function


def check_config(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if not app.config['HAS_CONFIG']:
			return redirect( url_for('setup') )
		return f(*args, **kwargs)
	return decorated_function


def check_for_commas(number):
	number = str(number)
	if ',' in number:
		number = number.replace(',', '.')
	return float(number)


def no_config(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if app.config['HAS_CONFIG']:
			return redirect( url_for('index') )
		return f(*args, **kwargs)
	return decorated_function


def login_or_test_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if not session.get('id') or not app.config['TESTING']:
			return redirect(url_for('login'))
		return f(*args, **kwargs)
	return decorated_function


@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404


def query_db(query, args=(), one=False):
	cur = g.db.execute(query, args)
	rv = [dict((cur.description[idx][0], value) for idx, value in enumerate(row)) for row in cur.fetchall()]
	return (rv[0] if rv else None) if one else rv


def connect_db():
	return sqlite3.connect(app.config['DATABASE'])


def init_db():
	with closing(connect_db()) as db:
		with open('roommates/schema.sql', 'r') as f:
			sql_commands = f.read()
			db.executescript(sql_commands)
		db.commit()


def add_line(s, key, line):
	return s + '\n' + key + " = '" + (line) + "'"
