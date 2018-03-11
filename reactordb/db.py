import sqlite3
import os.path

mods = {
    "CONTAINS": "%{cond}%",
    "STARTS": "%{cond}",
    "ENDS": "{cond}%"
}

connection = None
cursor = None
createdbcmd = """
CREATE TABLE reactordb (
	id integer PRIMARY KEY AUTOINCREMENT,
	pid integer,
	user string,
	tags text,
	pics text,
	date text,
	link string
);
"""


def connect(name='reactordb.db'):
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


# TODO: escape possible SQL injections
def escape(string):
    return string.strip().replace("'", "''")


def put(pid, user, tags, pics, date, link):
    pid = int(pid.strip())
    user = escape(user)
    tags = escape("|".join([x.strip() for x in tags]))
    pics = escape("|".join([x.strip() for x in pics]))
    date = escape(date.strip())
    link = escape(link)
    cursor.execute(f"INSERT INTO reactordb(pid, user, tags, pics, date, link) VALUES ('{pid}', '{user}', '{tags}', '{pics}', '{date}', '{link}')")


def get(what, text, mode="STARTS"):
    text = escape(text)
    data = cursor.execute(f"SELECT * FROM reactordb WHERE {what} LIKE '{mods[mode].replace('{cond}', text)}'")
    for row in data:
        yield row


def execute(command):
    data = cursor.execute(command)
    return data


def clear():
    try:
        cursor.execute("DROP TABLE IF EXISTS reactordb;")
    except:
        pass
    cursor.execute(createdbcmd)


def find_item(pid, link):
    pid, link = pid.strip(), link.strip()
    s = f"SELECT * FROM reactordb WHERE pid = '{escape(pid)}' AND link = '{escape(link)}'"
    res = cursor.execute(s).fetchall()
    return bool(res)
