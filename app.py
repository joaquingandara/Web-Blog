import sqlite3
from flask import Flask, render_template

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row #hace que las filas devueltas por las consultas SQL se comporten como diccionarios
    return conn

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