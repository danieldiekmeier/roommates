import sqlite3, os, roommates, unittest, tempfile, bcrypt
from datetime import datetime

class RoommatesTestCase(unittest.TestCase):
	def setUp(self):
		self.db_fd, roommates.app.config['DATABASE'] = tempfile.mkstemp()
		roommates.app.config['TESTING'] = True
		self.app = roommates.app.test_client()
		roommates.init_db()

		self.create_user({
			'name': 'Daniel',
			'last_name': 'Diekmeier',
			'mail': 'danieldiekmeier@gmail.com',
			'birthday': '1993-04-23',
			'password': 'default'
			})

		# create user whose birthday is today
		today = datetime.today()
		self.create_user({
			'name': 'Testo',
			'last_name': 'Superbirthday',
			'mail': 'supertesto@gmail.com',
			'birthday': str(today.year) + '-' + str(today.month) + '-' + str(today.day),
			'password': 'default'
			})

	def tearDown(self):
		os.close(self.db_fd)
		os.unlink(roommates.app.config['DATABASE'])

	def create_user(self, user):
		# set test user
		the_db = sqlite3.connect(roommates.app.config['DATABASE'])
		the_db.execute('INSERT INTO users (name, last_name, mail, birthday, password) VALUES (?, ?, ?, ?, ?)', [
				user["name"],
				user["last_name"],
				user["mail"],
				user["birthday"],
				bcrypt.hashpw(user["password"].encode('utf-8'), bcrypt.gensalt())
			])
		the_db.commit()
		the_db.close()

	def login(self, mail, password):
		return self.app.post('/login', data = dict(
				mail = mail,
				password = password
			), follow_redirects = True)

	def logout(self):
		return self.app.get('/logout', follow_redirects = True)


	# TESTS

	def test_no_session(self):
		# check if redirect works
		rv = self.app.get('/')
		assert rv.status_code == 302 and '/login' in rv.headers['location']

		rv = self.app.get('users')
		assert rv.status_code == 302 and '/login' in rv.headers['location']

	def test_login_logout(self):
		rv = self.login('danieldiekmeier@gmail.com', 'default')
		assert 'You are now logged in.' in rv.data

		rv = self.logout()
		assert 'You were logged out' in rv.data

		rv = self.login('lol@danieldiekmeier.de', 'default')
		assert 'Login nicht erfolgreich.' in rv.data

		rv = self.login('danieldiekmeier@gmail.com', 'defaultx')
		assert 'Login nicht erfolgreich.' in rv.data

	def test_list_users(self):
		self.login('danieldiekmeier@gmail.com', 'default')
		rv = self.app.get('users')
		self.logout()
		assert "Daniel" in rv.data

	def test_new_user(self):
		self.login('danieldiekmeier@gmail.com', 'default')

		user = {
			'name': 'Daniel',
			'last_name': 'Diekmeier',
			'mail': 'danieldiekmeier@gmail.com',
			'birthday': '1993-04-23',
			'password': 'default'
			}
		rv = self.app.post('/add_user', data = user, follow_redirects = True)
		assert str('The new user "' + user['name'] + ' ' + user['last_name'] + '" has been added.') in rv.data

		user = {
			'name': '',
			'last_name': 'Diekmeier',
			'mail': 'danieldiekmeier@gmail.com',
			'birthday': '1993-04-23',
			'password': 'default'
			}
		rv = self.app.post('/add_user', data = user, follow_redirects = True)
		assert 'Please fill out all the fields.' in rv.data

		self.logout()

	def test_delete_user(self):
		self.login('danieldiekmeier@gmail.com', 'default')

		rv = self.app.get('remove_user/2', follow_redirects = True)
		assert 'The user has been deleted.' in rv.data

		rv = self.app.get('remove_user/10', follow_redirects = True)
		assert 'No user with this id.' in rv.data

		self.logout()

if __name__ == '__main__':
	unittest.main()
