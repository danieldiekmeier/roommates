from roommates import app
from roommates.helpers import *
from roommates.classes import *

from flask import session, redirect, url_for, g, request, flash, render_template

date_format = "%Y-%m-%d"

@app.route("/messages/new", methods=['GET', 'POST'])
@login_required
def message_new():

	now = datetime.today()

	if request.method == 'POST' and request.form['message'] != '':
		g.db.execute('INSERT INTO messages (author, message, date) VALUES (?, ?, ?)', [
				session.get('id'),
				request.form["message"],
				now
			])
		g.db.commit()
		return redirect( url_for('index') )
	return redirect( url_for('index') )