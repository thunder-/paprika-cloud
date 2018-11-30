from flask import Blueprint, render_template, abort
from flask import Flask, g, flash
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import current_app
from flask_login import login_user
from flask import session
from datetime import date

from paprika_cloud.repositories.UserRepository import UserRepository
from paprika_cloud.templates.login.User import User

login = Blueprint('login', __name__, template_folder='templates')


@login.route('/login', methods=['GET', 'POST'])
def show():
    if request.method == 'GET':
        return render_template('login/login.html')

    username = request.form['username']
    password = request.form['password']

    # set session form variables, for failing
    session['login.username'] = username
    session['login.password'] = password

    remember_me = False
    if 'remember_me' in request.form:
        remember_me = True

    connector = current_app.connector

    user_repository = UserRepository(connector)
    user = user_repository.find_by_username(username)
    connector.close()

    registered_user = None
    if user:
        registered_user = User(user['id'], user['username'], user['password'], user['hashcode'])

    if registered_user is None:
        flash('Invalid username or password', 'danger')
        return redirect(url_for('login.show'))
    if not registered_user.check_password(password):
        flash('Invalid username or password', 'danger')
        return redirect(url_for('login.show'))
    login_user(registered_user, remember=remember_me)
    session['username'] = request.form['username']
    session['today'] = date.today().strftime("%d-%m-%Y")

    # remove session form variables, for failing
    if session.get('login.username'):
        session.pop('login.username')
        session.pop('login.password')

    return redirect(request.args.get('next') or url_for('index.show'))
