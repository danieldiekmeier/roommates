from roommates import app
from roommates.helpers import *
from roommates.classes import *

from flask import session, redirect, url_for, g, request, flash, render_template
import bcrypt

@app.route("/wiki")
@login_required
def wiki():
	g.user = User(session.get('id'))

	return render_template('wiki.html', user=g.user)

@app.route("/wiki/<category>/<key>")
@login_required
def wiki_page(category, key):
	g.user = User(session.get('id'))
	g.wiki = Wiki()

	if g.wiki.get_page(category, key):
		return render_template('wiki_page.html', user=g.user, page=g.wiki.get_page(category, key))
	else:
		return render_template('wiki_edit.html', values={'category': category, 'key': key, 'content': ''}, formaction='wiki_new')

@app.route("/wiki/new", methods=['GET', 'POST'])
@login_required
def wiki_new():

	if request.method == 'POST':
		for key, value in request.form.items():
			if value == '':
				flash('Please fill out all the fields.', 'error')
				return render_template('wiki_edit.html', values=request.form, formaction='wiki_new')
		g.db.execute('INSERT INTO wiki (category, key, content) VALUES (?, ?, ?)', [
				request.form["category"],
				request.form["key"],
				request.form["content"]
			])
		g.db.commit()
		flash('The new wiki page has been added.')
		return redirect(url_for('wiki_page', category=request.form["category"], key=request.form["key"]))

	return render_template('wiki_edit.html', values=[], formaction='wiki_new')

@app.route("/wiki/<category>/<key>/edit", methods=['GET', 'POST'])
@login_required
def wiki_edit(category, key):
	if request.method == 'POST':
		for key, value in request.form.items():
			if value == '':
				flash('Please fill out all the fields.', 'error')
				return render_template('wiki_edit.html', values=request.form, formaction='wiki_new')
		g.db.execute('UPDATE wiki SET category=?, key=?, content=? WHERE category=? and key=?', [
				request.form["category"],
				request.form["key"],
				request.form["content"],
				request.form["category"],
				request.form["key"]
			])
		g.db.commit()
		flash('The wiki page has been changed.')
		return redirect(url_for('wiki_page', category=request.form["category"], key=request.form["key"]))

	g.wiki = Wiki()

	return render_template('wiki_edit.html', values={'category': category, 'key': key, 'content': g.wiki.get_page(category, key)['md_content']}, formaction='wiki_edit')
