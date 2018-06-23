# all the imports
import os
import json

from flask import (Flask, abort, flash, g, redirect, render_template, request,
                   session, url_for)
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource

# configuration
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'admin'
try:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
except:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///flasker.db'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
api = Api(app)

db = SQLAlchemy(app)


class Entry(db.Model):
    __tablename__ = 'entries'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    text = db.Column(db.Text)

    def __repr__(self):
        return '<Entry id={id} title={title!r}>'.format(id=self.id, title=self.title)


def init_db():
    db.create_all()


class RestApi(Resource):
    def get(self):
        entries = Entry.query.order_by(Entry.id.desc()).all()
        return {e.id: {'title': e.title, 'text': e.text} for e in entries}


api.add_resource(RestApi, '/api/sample')


@app.route('/')
def show_entries():
    entries = Entry.query.order_by(Entry.id.desc()).all()
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    entry = Entry(title=request.form['title'], text=request.form['text'])
    db.session.add(entry)
    db.session.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


if __name__ == '__main__':
    app.run()
