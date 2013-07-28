import sqlite3
from roommates.helpers import query_db
from datetime import datetime
from markdown import markdown

date_format = "%Y-%m-%d"

class User:
	def __init__(self, id):
		user = query_db('SELECT * FROM users WHERE id = ?', [id], one=True)
		for key, value in user.items():
			setattr(self, key, value)
		return None

	def init_with_dict(self, user):
		for key, value in user.items():
			setattr(self, key, value)

	def days_to_birthday(self):
		today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)

		birthday = datetime.strptime(self.birthday, date_format)
		next_birthday = birthday.replace(year=today.year)
		if next_birthday < today:
			next_birthday = birthday.replace(next_birthday.year+1)
		return (next_birthday - today).days

	def expenses(self):
		roommates = query_db('SELECT COUNT(*) AS count FROM users', one=True)
		print roommates
		expenses = query_db('SELECT * FROM expenses ORDER BY amount DESC')

		for expense in expenses:
			expense['amount'] = expense['amount'] / ( roommates['count'] / 1.00)
		print expenses
		return expenses

class Wiki:
	def __init__(self):
		return None

	def get_all(self):
		return query_db('SELECT key FROM wiki ORDER BY key ASC')

	def get_page(self, key):
		page = query_db('SELECT * FROM wiki WHERE key = ?', [key], one=True)
		if page == None:
			return False
		else:
			page['md_content'] = page['content']
			page['content'] = markdown(page['content'])
			return page

