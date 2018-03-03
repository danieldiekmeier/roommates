from flask import request, g, redirect, url_for, render_template
import bcrypt

from roommates import app
from roommates.helpers import add_line, init_db, connect_db, no_config

import string
import random

@app.route('/setup', defaults={'step': 0},  methods=['GET', 'POST'])
@app.route('/setup/step/<int:step>', methods=['GET', 'POST'])
@no_config
def setup(step):
	if request.method == 'POST':
		if step == 1:
			# CREATE THE CONFIG.PY
			config_file = ''
			config_file = add_line(config_file, 'TITLE', request.form['title'])
			config_file = add_line(config_file, 'DATABASE', request.form['database'])
			config_file = add_line(config_file, 'CURRENCY', request.form['currency'])
			config_file = add_line(config_file, 'UPLOAD_FOLDER', request.form['upload_folder'])

			random_string = ''.join(random.choice( string.ascii_uppercase + string.ascii_lowercase + string.digits ) for x in range (24))
			config_file = add_line(config_file, 'SECRET_KEY', random_string)

			with open('roommates/config.py', 'w') as file:
				file.write(config_file)

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
				bcrypt.hashpw(request.form["password"].encode('utf-8'), bcrypt.gensalt())
			])
			g.db.commit()

		return redirect( url_for('setup', step=step+1) )


	else:
		return render_template('setup.html', step=step)
