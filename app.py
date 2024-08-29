import sqlite3
from flask import Flask, render_template
from werkzeug.exceptions import abort

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row #hace que las filas devueltas por las consultas SQL se comporten como diccionarios
    return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

app = Flask(__name__) #Create app instance

#'@' works as python decorator to wrapped function. 
# In particular the decorator turns a function into a flask view function.
# This function will respond to / requests via http
@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall() # fetchall() method to fetch all the rows of the query result.
    conn.close()
    return render_template('index.html',posts=posts) #Render_template helps you render html file located in /templates.
    #posts = posts returning post when index called

# IF an user want to access .../1 then the decorator will call post with 1 as argument.
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)