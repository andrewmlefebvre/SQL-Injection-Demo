import sqlite3
import os
from sqlite3 import Error
from flask import Flask, render_template, request, url_for, redirect

sqlite3.enable_callback_tracebacks(True)

app = Flask(__name__)


def connect(name):
    conn = None
    try:
        conn = sqlite3.connect(name)
        conn.isolation_level = None
    except Error as e:
        print(f"Error: {e}")
    return conn


def execute_select(conn, sql):
    try:
        c = conn.cursor()
        c.execute(sql)
        rows = c.fetchall()
        return rows
    except Error as e:
        print(f"Error: {e}")


def init_db(name):
    init_db_table_command = """
    CREATE TABLE IF NOT EXISTS item (
        id integer PRIMARY KEY AUTOINCREMENT,
        name text,
        description text,
        hiddenField text
    );
    """
    populate_db_command = [
    """INSERT INTO item (id, name, description, hiddenField) VALUES (1, 'item1', 'This is item 1', 'hidden message1');""",
    """INSERT INTO item (id, name, description, hiddenField) VALUES (2, 'item2', 'This is item 2', 'hidden message2');""",
    """INSERT INTO item (id, name, description, hiddenField) VALUES (3, 'item3', 'This is item 3', 'hidden message3');""",
    """INSERT INTO item (id, name, description, hiddenField) VALUES (4, 'item4', 'This is item 4', 'hidden message4');""",
    """INSERT INTO item (id, name, description, hiddenField) VALUES (5, 'item5', 'This is item 5', 'hidden message5');""",
    """INSERT INTO item (id, name, description, hiddenField) VALUES (6, 'item6', 'This is item 6', 'hidden message6');"""
    ]
    if not os.path.exists(name):
        open(name, 'w').close()
    try:
        conn = connect(name)
        conn.execute('DROP TABLE IF EXISTS item;')
        conn.commit()
        conn.execute(init_db_table_command)
        conn.commit()
        if len(execute_select(conn, 'SELECT * FROM item;')) == 0:
            for i in populate_db_command:
                conn.execute(i)
                conn.commit()
    except Error as e:
        print(f"Error: {e}")    



@app.route('/')
def index():
    return render_template('splash.html')


@app.route('/search', methods=['POST'])
def search():
    try:
        conn = connect('data.db')
        query = str(request.form['query'])
        print(query)
        sql = f"SELECT * FROM ITEM WHERE name = '{query}';"
        results = execute_select(conn, sql)
        return render_template('splash.html', results=results, query=query)
    except Error as e:
        print(f"Error: {e}")    


#  ', ' ', ' '); DROP TABLE IF EXISTS item; INSERT INTO item (id, name, description, hiddenField) VALUES (null, 'new
@app.route('/add', methods=['POST'])
def add():
    name = request.form.get('name')
    description = request.form.get('description')

    if not name or not description:
        return "Name and description are required!", 400

    try:
        conn = connect('data.db')
        sql = f"""INSERT INTO item (id, name, description, hiddenField) VALUES (null, '{name}', '{description}', 'hidden message6');"""
        conn.executescript(sql)
        conn.commit()
        return redirect(url_for('index'))
    except Error as e:
        print(f"Error: {e}")    
        return "An error occurred while adding the entry", 500


if __name__ == '__main__':
    init_db('data.db')
    app.run(debug=False)