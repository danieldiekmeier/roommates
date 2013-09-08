from roommates import app
from roommates.helpers import *
from roommates.classes import *

from flask import session, redirect, url_for, g, request, flash, render_template, abort

@app.route("/purchases", methods=['GET'])
@login_required
def purchases():
	purchase_ids = query_db('SELECT id FROM purchases ORDER BY id DESC')
	purchases = []
	for purchase_id in purchase_ids:
		temp_purchase = Purchase(purchase_id['id'])
		purchases.append(temp_purchase)
	return render_template('purchases.html', purchases=purchases)

@app.route('/purchases/add', methods=['GET', 'POST'])
@login_required
def purchases_add():
	if request.method == 'POST':
		for key, value in request.form.items():
			if value == '':
				flash('Please fill out all the fields.', 'error')
				return render_template('purchases_add.html', values=request.form)
		amount = check_for_commas( request.form['amount'] )
		g.db.execute('INSERT INTO purchases (title, amount, date) VALUES (?, ?, ?)', [
				request.form["title"],
				amount,
				request.form["date"]
			])
		g.db.commit()
		flash('The new purchase "' + request.form['title'] + '" has been added.')
	return render_template('purchases_add.html', values=[])

@app.route('/purchases/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def purchases_edit(id):
	if request.method == 'POST':
		for key, value in request.form.items():
			if value == '':
				flash('Please fill out all the fields.', 'error')
				return render_template('purchases_add.html', values=request.form)
		amount = check_for_commas( request.form['amount'] )
		g.db.execute('UPDATE purchases SET title=?, amount=?, date=? WHERE id=?', [
				request.form["title"],
				amount,
				request.form["date"],
				id
			])
		g.db.commit()
		flash('The purchase "' + request.form['title'] + '" has been edited.')
		return redirect( url_for('purchases') )

	else:
		purchase = query_db('SELECT * FROM purchases WHERE id = ?', [id], one=True)
		if purchase:
			return render_template('purchases_edit.html', values=purchase)
		else:
			abort(404)

@app.route('/purchases/delete/<int:id>', methods=['GET'])
@login_required
def purchases_delete(id):
	g.db.execute('DELETE FROM purchases WHERE id=?', [id])
	g.db.commit()
	flash('The receipt has been deleted.')
	return redirect( url_for('purchases') )