from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, jsonify
import sqlite3, datetime, bcrypt
from contextlib import closing # for database-things

import os
import codecs

from roommates import app
from roommates.helpers import *
from roommates.classes import *

import bcrypt

import string
import random

@app.route('/setup', defaults={'step': 0},  methods=['GET', 'POST'])
@app.route('/setup/step/<int:step>', methods=['GET', 'POST'])
@no_config
def setup(step):
	if request.method == 'POST':
		if step == 1:

			# CREATE THE CONFIG.PY
			config_file = '# -*- coding: utf-8 -*-'
			config_file = add_line(config_file, 'TITLE', request.form['title'])
			config_file = add_line(config_file, 'DATABASE', request.form['database'])
			config_file = add_line(config_file, 'CURRENCY', request.form['currency'])
			config_file = add_line(config_file, 'UPLOAD_FOLDER', request.form['upload_folder'])

			random_string = ''.join(random.choice( string.ascii_uppercase + string.ascii_lowercase + string.digits ) for x in range (24))
			config_file = add_line(config_file, 'SECRET_KEY', random_string)


			output_file = codecs.open('roommates/config.py', 'w+', encoding='utf-8')
			output_file.write(unicode(config_file))

			# LOAD THE CONFIG.PY
			app.config.from_pyfile('config.py')

			# CREATE THE DATABASE
			init_db()

			# CONNECT WITH DATABASE
			g.db = connect_db()

			# ADD THE USER
			g.db.execute('INSERT INTO users (name, last_name, mail, birthday, password) VALUES (?, ?, ?, ?, ?)', [
				request.form["name"],
				request.form["last_name"],
				request.form["mail"],
				request.form["birthday"],
				bcrypt.hashpw(str(request.form["password"]), bcrypt.gensalt())
			])
			g.db.commit()

		return redirect( url_for('setup', step=step+1) )


	else:
		return render_template('setup.html', step=step)