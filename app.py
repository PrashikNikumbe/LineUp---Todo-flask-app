from flask import Flask, render_template, request, redirect,session, json,redirect,url_for
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///LineUp.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'This is a secret key required for session'
db = SQLAlchemy(app)
class Todoids(db.Model):
    todoId = db.Column(db.String(20), primary_key=True)

class Todolist(db.Model):
    sno = db.Column(db.Integer,primary_key=True )
    todoName = db.Column(db.String(200), nullable=False)
    todoDesc = db.Column(db.String(500), nullable=False)
    todoPr = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    FktodoId =  db.Column(db.String(20))


@app.route('/', methods=['GET', 'POST'])
def start():
    return redirect(url_for("index"))

@app.route('/index.html', methods=['GET', 'POST'])
def index():
    if request.method=='POST':

        if 'newTodoId' in request.form:
            formTodoId = request.form['newTodoId']
            id  = Todoids.query.filter_by(todoId = formTodoId).first()

            if id is not None:
                return render_template('index.html',check1 = True,check2=False)
            else:
                todoId = Todoids(todoId=formTodoId)
                db.session.add(todoId)
                db.session.commit()
                session['ownerId'] =  formTodoId
                return redirect(url_for("addTodo"))
        elif 'TodoId' in request.form:
            formTodoId = request.form['TodoId']
            id  = Todoids.query.filter_by(todoId = formTodoId).first()

            if id is None:
                return render_template('index.html',check1 = False,check2 = True)
            else:
                session['ownerId'] =  formTodoId
                return redirect(url_for("addTodo"))

    return render_template('index.html',check1 = False,check2=False)

@app.route('/index.html#About')
def About():
    return render_template('index.html#About')

@app.route('/addTodo.html',methods=['GET', 'POST'])
def addTodo():

    if 'ownerId' not in session:
        return render_template('addTodo.html',check=True)
    else:
        if request.method=='POST':
            formTodoName = request.form['TodoName']
            formTodoDesc = request.form['TodoDesc']
            formTodoPr = request.form['TodoPr']
            item = Todolist(todoName=formTodoName ,todoDesc=formTodoDesc,todoPr=formTodoPr,FktodoId=session['ownerId'])
            db.session.add(item)
            db.session.commit()
            return redirect(url_for("todoList"))
        return render_template('addTodo.html',check=False)
    
@app.route('/todoList.html',methods=['GET', 'POST'])
def todoList():
    if 'ownerId' not in session:
        return render_template('todoList.html',check1=True,check2=False)
    else :
        if request.method=='POST':
            formTodoName = request.form['searchTodoName']
            allTodo = Todolist.query.filter_by(FktodoId = session['ownerId'],todoName=formTodoName).order_by(Todolist.todoPr).all()
            if len(allTodo)==0:
                return render_template('todoList.html',allTodo = allTodo,check1=False,check2=True)
            else:
                return render_template('todoList.html',allTodo = allTodo,check1=False,check2=False)
        else:
            allTodo = Todolist.query.filter_by(FktodoId = session['ownerId']).order_by(Todolist.todoPr).all()
            return render_template('todoList.html',allTodo = allTodo,check1=False,check2=False)

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        formTodoName = request.form['TodoName']
        formTodoDesc = request.form['TodoDesc']
        formTodoPr = request.form['TodoPr']
        todo = Todolist.query.filter_by(sno=sno).first()
        todo.todoName = formTodoName
        todo.todoDesc = formTodoDesc
        todo.todoPr = formTodoPr
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for("todoList"))

    todo = Todolist.query.filter_by(sno=sno).first()
    id = todo.FktodoId
    if  id == session['ownerId']:
        return render_template('updateTodo.html', todo=todo,check=False)
    else:
        return render_template('updateTodo.html', todo=todo,check=True)


@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todolist.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("todoList"))

@app.route('/emptylist')
def deleteall():
    allTodo = Todolist.query.filter_by(FktodoId = session['ownerId']).all()
    for i in allTodo:
        db.session.delete(i)
        db.session.commit()
    return redirect(url_for("todoList"))




if __name__ == "__main__":
    app.run(debug=True)
