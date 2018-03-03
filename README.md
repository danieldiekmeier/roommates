# Roommates

![screenshot](https://s3-eu-west-1.amazonaws.com/51e3d489f1e/2013-10-03-06-52-35-524da0d39c392.png)

Organize your shared living arrangement.


## Installation

It's simple, really. If you want to check it out locally, try this:

```
git clone https://github.com/danieldiekmeier/roommates
cd roommates
pipenv install
pipenv run python runserver.py
```

Then go to http://127.0.0.1:1337. Roommates comes with a simple setup where you can enter everything Roommates needs to know and the database will automatically be created.

If you want to install it on your server, the excact installation may differ, but the Flask documentation for deploying is quite good: http://flask.pocoo.org/docs/deploying/


## config.py

If you have trouble with creating a `config.py` with the setup, here is what it should consist of:

```
TITLE = 'Roommates'
DATABASE = 'roommates.db'
CURRENCY = '€'
UPLOAD_FOLDER = '/Users/<You>/dev/python/roommates/roommates/uploads'
SECRET_KEY = 'this has to be extremely seecret'
```


## Database

The `roommates` Subfolder contains a schema.sql that can help you setting up the SQLite-Database if the setup doesn't work.
