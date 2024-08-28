from flask import Flask, render_template

app = Flask(__name__) #Create app instance

#'@' works as python decorator to wrapped function. 
# In particular the decorator turns a function into a flask view function.
# This function will respond to / requests via http
@app.route('/')
def index():
    return render_template('index.html') #Render_template helps you render html file located in /templates.