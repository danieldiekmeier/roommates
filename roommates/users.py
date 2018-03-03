from roommates import app
from roommates.helpers import login_required, query_db
from roommates.classes import User

from flask import redirect, url_for, g, request, flash, render_template
import bcrypt

@app.route("/users", methods=['GET'])
@login_required
def users():
	user_ids = query_db('SELECT id FROM users ORDER BY id ASC')
	users = []
	for user_id in user_ids:
		temp_user = User(user_id['id'])
		users.append(temp_user)
	return render_template('users.html', users = users)


@app.route("/users/add", methods=['GET', 'POST'])
@login_required
def users_add():
	if request.method == 'POST':
		for key, value in request.form.items():
			if value == '':
				flash('Please fill out all the fields.', 'error')
				return render_template('users_add.html', values=request.form)
		g.db.execute('INSERT INTO users (name, last_name, mail, birthday, password) VALUES (?, ?, ?, ?, ?)', [
				request.form["name"],
				request.form["last_name"],
				request.form["mail"],
				request.form["birthday"],
				bcrypt.hashpw(request.form["password"].encode('utf-8'), bcrypt.gensalt())
			])
		g.db.commit()
		flash('The new user "' + request.form['name'] + ' ' + request.form['last_name'] + '" has been added.')
	return render_template('users_add.html', values=[])


@app.route("/remove_user/<id>", methods=['GET'])
@login_required
def remove_user(id):
	user = query_db('SELECT id from users WHERE id = ?', [id], one = True)
	if user:
		g.db.execute('DELETE FROM users WHERE id = ?', [id])
		g.db.commit()
		flash('The user has been deleted.')
	else:
		flash('No user with this id.', 'error')
	return redirect(url_for('users'))
