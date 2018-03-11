import sqlite3
import os.path

connection = None
cursor = None
createdbcmd = """
CREATE TABLE SongsWords (
	ID integer PRIMARY KEY AUTOINCREMENT,
	Author string,
	Album string,
	Title string,
	Text text
);
"""


def connect(name='words.db'):
    global connection, cursor
    if os.path.isfile(name):
        new_db = False
    else:
        new_db = True
    connection = sqlite3.connect(name)
    cursor = connection.cursor()
    if new_db:
        cursor.execute(createdbcmd)


def close():
    connection.commit()
    connection.close()

def commit():
    connection.commit()


# TODO: escape possible SQL injections
def escape(string):
    return string.strip().replace("'", "''")


def put(Author, Album, Title, Text):
    Author = escape(Author)
    Album = escape(Album)
    Title = escape(Title)
    Text = escape(Text)
    cursor.execute(
        f"INSERT INTO SongsWords(Author, Album, Title, Text) VALUES ('{Author}', '{Album}', '{Title}', '{Text}')")


def get(what, field, text):
    text = escape(text)
    data = cursor.execute(f"SELECT {what} FROM SongsWords WHERE {field} LIKE '{text}%'")
    for row in data:
        yield row


def get_all():
    for row in get("*", "Author", ""):
        yield row


def execute(command):
    data = cursor.execute(command)
    return data


def clear():
    try:
        cursor.execute("DROP TABLE 'SongsWords'")
    except:
        pass
    cursor.execute(createdbcmd)


def find_item(Author, Title):
    Author, Title = Author.strip(), Title.strip()
    s = f"SELECT * FROM SongsWords WHERE Author = '{escape(Author)}' AND Title = '{escape(Title)}'"
    res = cursor.execute(s).fetchall()
    return bool(res)


def find_same(what, eq):
    query = f"{what.strip()} LIKE '{eq.strip()}%'"
    s = f"SELECT * FROM SongsWords WHERE {query}"
    res = cursor.execute(s).fetchall()
    return len(res) < 5 and bool(res)