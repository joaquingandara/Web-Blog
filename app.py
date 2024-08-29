import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
import secrets
#The global request object to access incoming request data that will be submitted via an HTML form.
#The url_for() function to generate URLs.
#The flash() function to flash a message when a request is processed.
#The redirect() function to redirect the client to a different location.

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
app.config['SECRET_KEY'] = secrets.token_bytes(16)  

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

#get y post. So, user can access form and send data.
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST': #handle the incoming POST request 
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
#If post handle update. If get show the post form asociated with id.
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    if request.method == 'POST': #handle the incoming POST request 
        name = request.form['name']
        email = request.form['email']
        textbox = request.form['textbox']
        #action to be performed with the contact form.
        return redirect(url_for('index'))
    return render_template('contact.html')
