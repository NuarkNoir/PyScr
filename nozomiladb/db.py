import sqlite3
import os.path

connection = None
cursor = None
createdbcmd = f"""
CREATE TABLE NozomiLa(
	id integer PRIMARY KEY AUTOINCREMENT,
	characters text,
	series text,
	artists text,
	tags text,
	image text,
	postlink text,
	downloaded integer
);
"""


def connect(name='nozomila.db'):
    global connection, cursor
    if os.path.isfile(name):
        new_db = False
    else:
        new_db = True
    connection = sqlite3.connect(name)
    cursor = connection.cursor()
    if new_db:
        cursor.execute(createdbcmd)


def commit():
    connection.commit()


def close():
    connection.commit()
    connection.close()


def escape(string):
    return string.strip().replace("'", "''")


def put(characters, series, artists, tags, image, postlink):
    characters, series, artists, tags, image, postlink = escape(characters), escape(series), escape(artists), escape(tags), escape(image), escape(postlink)
    cursor.execute(f"INSERT INTO NozomiLa(characters, series, artists, tags, image, postlink) VALUES ('{characters}', '{series}', '{artists}', '{tags}', '{image}', '{postlink}')")


def get(what, field, text):
    text = escape(text)
    data = cursor.execute(f"SELECT {what} FROM NozomiLa WHERE {field} LIKE '{text}%'")
    for row in data:
        yield row


def get_all():
    for row in cursor.execute(f"SELECT * FROM NozomiLa"):
        yield row


def execute(command):
    data = cursor.execute(command)
    return data


def clear():
    try:
        cursor.execute("DROP TABLE IF EXISTS NozomiLa;")
    except:
        pass
    cursor.execute(createdbcmd)


def find_item(postlink):
    s = f"SELECT * FROM NozomiLa WHERE postlink = '{escape(postlink)}'"
    res = cursor.execute(s).fetchall()
    return bool(res)