# all the imports
from __future__ import with_statement
import sys
sys.path.append( './models')

from contextlib import closing
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
import user_auth
from user_auth import UserAuth
from user_auth import check_password_hash





# create our little application :)
app = Flask(__name__)

# configuration
# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))

app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])
    
@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.route('/')
def show_entries():
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)
    
@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    g.db.commit()
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
            print(session)
            session['logged_in'] = True
            print(session)
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)
    
@app.route('/logout')
def logout():
    print(session)
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))
    


# FOR NEW USERS TO SIGN UP
@app.route('/sign_up', methods=['GET','POST'])
def sign_up():
    # cur = g.db.execute('select email from users order by id desc')
    # users = [dict(user=row[0]) for row in cur.fetchall()]
    # import code; code.interact(local=dict(globals(), **locals()))
    if(request.method == "POST"):
        if request.form['email'] != '' and request.form['password'] != '':
            user = UserAuth(request.form['email'],request.form['password'])
            password_hash = user.pw_hash
            
            print(request.form['email']+' '+password_hash)
            g.db.execute('insert into users (email, password) values (?, ?)',
                 [request.form['email'], password_hash ])
            g.db.commit()
            print('after commit')
       
        else:
            print(session)
            session['logged_in'] = True
            print(session)
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    else:
        if session.get('logged_in'):
            flash('you must sign out')
            return redirect(url_for('show_entries'))
        else:
            return render_template('sign_up.html', error=None)
        # g.db.execute('insert into entries (title, text) values (?, ?)',
        #              [request.form['title'], request.form['text']])
        # g.db.commit()
        # flash('New entry was successfully posted')
        # return redirect(url_for('show_entries'))
    print('end of function')
    return redirect(url_for('show_entries'))


@app.route('/users', methods=['GET'])
def users():
    cur = g.db.execute('select email from users order by id desc')
    users = [dict(email=row[0]) for row in cur.fetchall()]
    print(users)
    return render_template('users.html', users=users)
        
        # g.db.execute('insert into entries (title, text) values (?, ?)',
        #              [request.form['title'], request.form['text']])
        # g.db.commit()
        # flash('New entry was successfully posted')
        # return redirect(url_for('show_entries'))
       


if(__name__ == '__main__'):
    app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))
