import sqlite3
from roommates.helpers import query_db
from datetime import datetime
from markdown import markdown
import arrow

date_format = "%Y-%m-%d"

class User:
	def __init__(self, id):
		user = query_db('SELECT * FROM users WHERE id = ?', [id], one=True)
		for key, value in user.items():
			setattr(self, key, value)
		return None

	def __str__(self):
		return unicode(self.name) + ' ' + unicode(self.last_name)
	def __repr__(self):
		return self.__str__()

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

		expenses = query_db('SELECT * FROM expenses ORDER BY amount DESC')

		for expense in expenses:
			expense['amount'] = expense['amount'] / ( roommates['count'] / 1.00)
		return expenses

	def spending(self):
		try:
			spending_sum = query_db('SELECT SUM(amount) AS sum FROM receipts', one=True)['sum']
			self._spending =  query_db('SELECT SUM(amount) AS sum FROM receipts WHERE user = ?', [self.id], one=True)['sum'] - (spending_sum/count_users())
			return self._spending
		except TypeError:
			return 0

	def errand(self):

		week = datetime.now().isocalendar()[1]

		users = query_db('SELECT * FROM users ORDER BY id ASC')
		number_of_users = len(users)

		user_number = next(index for (index, d) in enumerate(users) if d["id"] == self.id)

		part_list = range(1, number_of_users+1)
		list = []
		list.append(part_list[:])

		for i in xrange(number_of_users-1):
			part_list.append(part_list.pop(0))
			list.append(part_list[:])

		errand_number = list[user_number-1][(week % number_of_users)-1] - 1

		errand_ids = query_db('SELECT id FROM errands ORDER BY id ASC')

		print errand_ids

		errands = []
		for errand_id in errand_ids:
			errand = Errand( errand_id['id'] )
			errands.append(errand)

		try:
			return errands[errand_number]
		except IndexError:
			return "None"

	def reminders(self):
		roommates = query_db('SELECT id FROM users')

		reminders = []

		for roommate in roommates:
			user = User(roommate['id'])
			if user.days_to_birthday() < 30:
				reminder = Reminder()
				reminder.birthday(user)
				reminders.append(reminder)

		return reminders

def list_users():
	user_ids = query_db('SELECT * FROM users ORDER BY id ASC')
	users = []
	for user_id in user_ids:
		user = User(user_id['id'])
		users.append(user)
	return users

def count_users():
	return query_db('SELECT COUNT(id) AS count FROM users', one=True)['count']


class Errand:
	def __init__(self, id):
		errand = query_db('SELECT * FROM errands WHERE id = ?', [id], one=True)
		for key, value in errand.items():
			setattr(self, key, value)
		return None
	def __str__(self):
		return self.title
	def __unicode__(self):
		return self.title
	def __repr__(self):
		return self.title.encode('utf-8')

class Reminder:
	def __init__(self):
		return None
	def birthday(self, user):
		self.type = 'birthday'
		self.user = user

class Wiki:
	def __init__(self):
		return None

	def get_all(self):
		return query_db('SELECT key FROM wiki ORDER BY key ASC')

	def get_page(self, key):
		return Page(key)

class Page:
	def __init__(self, param):
		if param == unicode(param):
			key = param
			page = query_db('SELECT * FROM wiki WHERE key = ?', [key], one=True)
		else:
			id = param
			page = query_db('SELECT * FROM wiki WHERE id = ?', [id], one=True)

		if page == None:
			self.exists = False
			return None
		else:
			self.exists = True
			for key, value in page.items():
				setattr(self, key, value)
			self.md_content = self.content
			self.content = markdown(self.content)
		return None

	def attached_files(self):
		files = query_db('SELECT id FROM uploads WHERE wiki_id = ?', [self.id])
		if files == None:
			return False
		else:
			files_list = []
			for file in files:
				files_list.append( File(file['id']) )
			return files_list

class File:
	def __init__(self, id):
		file = query_db('SELECT * FROM uploads WHERE id = ?', [id], one=True)
		for key, value in file.items():
			setattr(self, key, value)
		return None

class Message:
	def __init__(self, id):
		message = query_db('SELECT * FROM messages WHERE id = ?', [id], one=True)
		self.message = message['message']
		self.author = User(message['author'])
		self.datetime = datetime.strptime(message['date'], '%Y-%m-%d %H:%M:%S.%f')
		return None
	def __str__(self):
		return unicode(self.author.name) + ': ' + unicode(self.message)



class Purchase:
	def __init__(self, id):
		purchase = query_db('SELECT * FROM purchases WHERE id = ?', [id], one=True)
		self.id = purchase['id']
		self.title = purchase['title']
		self.amount = purchase['amount']
		self.date = arrow.get(purchase['date'], 'YYYY-MM-DD')
		return None
	def __str__(self):
		return unicode(self.author.name) + ': ' + unicode(self.purchase)
	def current_value(self):
		# today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
		today = arrow.now('Europe/Berlin').replace(hour=0, minute=0, second=0, microsecond=0)

		temp_date = self.date
		months = 0

		# if it is less than a month old
		if temp_date.month == today.month and temp_date.year == today.year:
			return self.amount

		while temp_date < today:
			temp_date = temp_date.replace(months=+1)
			months += 1

		if months >= 30:
			return 0
		else:
			return self.amount*0.95**months

class Receipt:
	def __init__(self, id):
		receipt = query_db('SELECT * FROM receipts WHERE id = ?', [id], one=True)
		self.id = receipt['id']
		self.title = receipt['title']
		self.amount = receipt['amount']
		self.user = User(receipt['user'])
		self.date = datetime.strptime(receipt['date'], '%Y-%m-%d')
		return None
