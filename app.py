from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy # for database
'''
First we import the Flask class. An instance of this calss will be our WSGI application.The Web Server Gateway Interface (WSGI, pronounced whiskey or WIZ-ghee) is a simple calling convention for web servers to forward requests to web applications or frameworks written in the Python programming language.
'''

# create instance of Flask class with the first argument being the name of the app's module or package; __name__ is a shortcut for this in most cases; needed so Flask knows where to look for resources 
app = Flask(__name__)

# database configuration variable
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite' # path to database with sqlite file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) # create database instance and passing the app into it

# create a model for the database, create a Todo class that inherits from db.Model, give it three columns with appropriate data types
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean) 

db.create_all() # create and initialize database

# route() decorator tells Falsk what URL should trigger our function
'''
@app.get("/") is equivalent to @app.route("/", methods=["GET"])
And since ["GET"] is the default, this is equivalent to @app.route("/")
'''

@app.route("/")

# this function returns the message to be displayed on user's browser; default content type is HTML, so HTML in the string will be rendered by the browser
def home():
    todo_list = db.session.query(Todo).all() # retrieve all Todo items
    return render_template("base.html", todo_list=todo_list) # render using index.html template

@app.post("/add")
def add():
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("home"))

# here we query a particular todo item by the id
@app.get("/update/<int:todo_id>")
def update(todo_id):
    todo = db.session.query(Todo).filter(Todo.id == todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("home"))

@app.get("/delete/<int:todo_id>")
def delete(todo_id):
    todo = db.session.query(Todo).filter(Todo.id == todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
