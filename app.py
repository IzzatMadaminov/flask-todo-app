from re import error
from typing import final
from flask import Flask, render_template, request, redirect, url_for, abort, jsonify
from flask.globals import session
from flask_sqlalchemy import SQLAlchemy
import sys
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://izzat:Izzat!8897@localhost:5432/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app, session_options={"expire_on_commit": False})

migrate = Migrate(app, db)


class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable=False)

    def __repr__(self):
        return f'<Todo {self.id} {self.description}'

class TodoList(db.Model):
    __tablename__ = 'todolists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    todos = db.relationship('Todo', backref='list', cascade='all, delete', lazy=True)

@app.route('/')
def index():
    return redirect(url_for('lists_todos', list_id=1)) 

@app.route('/lists/<list_id>')
def lists_todos(list_id):
    return render_template('index.html',
    lists = TodoList.query.all(),
    active_list = TodoList.query.get(list_id), 
    todos = Todo.query.filter_by(list_id=list_id).order_by('id')\
        .all())

@app.route('/lists/create', methods=['POST'])
def create_list():
    error = False
    try:
        name = request.form.get('name', '')
        list = TodoList(name=name)
        db.session.add(list)
        db.session.commit()
    except:
        db.session.rollback()
        print(sys.exc_info())
        error = True
    finally:
        db.session.close()
    if error:
        abort(400)
    else:
        return redirect(url_for('index'))

@app.route('/lists/<list_id>/set-completed', methods=['POST'])
def set_completed_list(list_id):
    error = False
    try:
        completed = request.get_json()['completed']
        list = TodoList.query.get(list_id)
        list.completed = completed
        list.todos.completed = completed
        for todo in list.todos:
            todo.completed = completed
        db.session.commit()
    except:
        db.session.rollback()
        print(sys.exc_info())
        error = True
    finally:
        db.session.close()
    if error:
        abort(400)
    else:
        return redirect(url_for('index'))

@app.route('/lists/<list_id>', methods=['DELETE'])
def delete_list(list_id):
    try:
        list = TodoList.query.get(list_id)
        db.session.delete(list)
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return jsonify({
        'success': True
    })

@app.route('/lists/<list_id>/todos/create', methods=['POST'])
def create_todo(list_id):
    error = False
    try:
        list = TodoList.query.get(list_id)
        description = request.form.get('description', '') #default value = ''
        todo = Todo(description = description)
        list.todos.append(todo)
        db.session.commit()
    except:
        db.session.rollback()
        print(sys.exc_info())
        error = True
    finally:
        db.session.close()
    if error:
        abort(400)
    else:
        return redirect(url_for('index'))

@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id):
    try:
        completed = request.get_json()['completed']
        todo = Todo.query.get(todo_id)
        todo.completed = completed
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))

@app.route('/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    try:
        todo = Todo.query.get(todo_id)
        db.session.delete(todo)
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return jsonify({'success': True})