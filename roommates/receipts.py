from roommates import app
from roommates.helpers import *
from roommates.classes import *

from flask import session, redirect, url_for, g, request, flash, render_template, abort

@app.route("/receipts", methods=['GET'])
@login_required
def receipts():
	receipt_ids = query_db('SELECT id FROM receipts ORDER BY date DESC')
	receipts = []
	for receipt_id in receipt_ids:
		temp_receipt = Receipt(receipt_id['id'])
		receipts.append(temp_receipt)
	return render_template('receipts.html', receipts=receipts)

@app.route('/receipts/add', methods=['GET', 'POST'])
@login_required
def receipts_add():
	if request.method == 'POST':
		for key, value in request.form.items():
			if value == '':
				flash('Please fill out all the fields.', 'error')
				return render_template('receipts_add.html', values=request.form)
		amount = check_for_commas( request.form['amount'] )
		g.db.execute('INSERT INTO receipts (title, amount, user, date) VALUES (?, ?, ?, ?)', [
				request.form['title'],
				amount,
				request.form['user'],
				request.form['date']
			])
		g.db.commit()
		flash('The new receipt "' + request.form['title'] + '" has been added.')
	return render_template('receipts_add.html', values=[], users=list_users())

@app.route('/receipts/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def receipts_edit(id):
	if request.method == 'POST':
		for key, value in request.form.items():
			if value == '':
				flash('Please fill out all the fields.', 'error')
				return render_template('receipts_add.html', values=request.form)
		amount = check_for_commas( request.form['amount'] )
		g.db.execute('UPDATE receipts SET title=?, amount=?, user=?, date=? WHERE id=?', [
				request.form["title"],
				amount,
				request.form['user'],
				request.form["date"],
				id
			])
		g.db.commit()
		flash('The receipt "' + request.form['title'] + '" has been edited.')
		return redirect( url_for('receipts') )

	else:
		receipt = query_db('SELECT * FROM receipts WHERE id = ?', [id], one=True)
		if receipt:
			return render_template('receipts_edit.html', values=receipt, users=list_users())
		else:
			abort(404)

@app.route('/receipts/delete/<int:id>', methods=['GET'])
@login_required
def receipts_delete(id):
	g.db.execute('DELETE FROM receipts WHERE id=?', [id])
	g.db.commit()
	flash('The receipt has been deleted.')
	return redirect( url_for('receipts') )
