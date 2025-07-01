import sqlite3
from flask import Flask, render_template
from werkzeug.exceptions import abort

def get_db_connection():
    con = sqlite3.connect('database.db')
    con.row_factory = sqlite3.Row
    return con

app = Flask(__name__)

@app.route('/')
def index():
    con = get_db_connection()
    users = con.execute('SELECT * from users').fetchall()
    con.close()
    return render_template('index.html', users=users)

@app.route('/<int:user_id>')
def user(user_id):
    user = get_user(user_id)
    return render_template('user.html', user=user)

def get_user(id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM users WHERE id = ?',
                        (id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

if __name__ == '__main__':
    app.run(debug=True)

