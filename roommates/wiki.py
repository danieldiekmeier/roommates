from roommates import app
from roommates.helpers import *
from roommates.classes import *

from flask import session, redirect, url_for, g, request, flash, render_template, send_from_directory
import bcrypt
import os
from werkzeug import secure_filename
import hashlib
from datetime import datetime

@app.route("/wiki")
@login_required
def wiki():
	g.user = User(session.get('id'))

	g.wiki = Wiki()

	return render_template('wiki.html', user=g.user, wiki=g.wiki)

@app.route("/wiki/<key>")
@login_required
def wiki_page(key):
	g.user = User(session.get('id'))
	g.wiki = Wiki()

	if g.wiki.get_page(key).exists:
		return render_template('wiki_page.html', user=g.user, page=g.wiki.get_page(key))
	else:
		return render_template('wiki_edit.html', values={'key': key, 'content': ''}, formaction='wiki_new')

@app.route("/wiki/new", methods=['GET', 'POST'])
@login_required
def wiki_new():
	if request.method == 'POST':
		for key, value in request.form.items():
			if value == '':
				flash('Please fill out all the fields.', 'error')
				return render_template('wiki_edit.html', values=request.form, formaction='wiki_new')
		g.db.execute('INSERT INTO wiki (key, content) VALUES (?, ?)', [
				request.form["key"],
				request.form["content"]
			])
		g.db.commit()
		flash('The new wiki page has been added.')
		return redirect(url_for('wiki_page', key=request.form["key"]))

	return render_template('wiki_edit.html', values=[], formaction='wiki_new')

@app.route("/wiki/<key>/edit", methods=['GET', 'POST'])
@login_required
def wiki_edit(key):
	if request.method == 'POST':
		for key, value in request.form.items():
			if value == '':
				flash('Please fill out all the fields.', 'error')
				return render_template('wiki_edit.html', values=request.form, formaction='wiki_new')
		g.db.execute('UPDATE wiki SET key=?, content=? WHERE key=?', [
				request.form["key"],
				request.form["content"],
				request.form["key"]
			])
		g.db.commit()
		flash('The wiki page has been changed.')
		return redirect(url_for('wiki_page', key=request.form["key"]))

	g.wiki = Wiki()

	return render_template('wiki_edit.html', values={'key': key, 'content': g.wiki.get_page(key).md_content}, formaction='wiki_edit')

@app.route('/wiki/upload/<int:id>', methods=['GET', 'POST'])
@login_required
def wiki_upload(id):
	if request.method == 'POST':
		file = request.files['file']

		if request.form["description"] == '':
			description = file.filename.rsplit('.', 1)[0]
		else:
			description = request.form["description"]

		if file:
			page = Page(id)
			filename = secure_filename(file.filename)
			temp_filename = filename

			if not os.path.exists( os.path.join(app.config['UPLOAD_FOLDER'], page.key )):
				os.makedirs( os.path.join(app.config['UPLOAD_FOLDER'], page.key ) )


			i = 2

			while os.path.exists( os.path.join(app.config['UPLOAD_FOLDER'], page.key, filename) ):
				filename = temp_filename.rsplit('.', 1)[0] + '-' + str(i) + '.' + temp_filename.rsplit('.', 1)[1]
				i += 1

			file.save(os.path.join(app.config['UPLOAD_FOLDER'], page.key, filename))

			flash('Saved new file')

			g.db.execute('INSERT INTO uploads (wiki_id, description, filename) VALUES (?, ?, ?)', [
				id,
				description,
				filename
			])
			g.db.commit()

	page = Page(id)
	return render_template('wiki_upload.html', id=id, values=[], page=page)

@app.route('/wiki/files/<key>/<filename>')
def uploaded_file(key, filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'], key + '/' + filename)