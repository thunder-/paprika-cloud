from flask import Blueprint, render_template, abort
from flask import Flask, g, flash
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import current_app
from flask import session
import uuid

from paprika_cloud.repositories.UserRepository import UserRepository
from paprika_cloud.templates.login.User import User

password = Blueprint('password', __name__, template_folder='templates')


@password.route('/password', methods=['GET', 'POST'])
def show():
    if request.method == 'GET':
        return render_template('password/password.html')

    connector = current_app.connector
    user_repository = UserRepository(connector)

    password = request.form['password']
    new_password = request.form['new_password']
    repeat = request.form['repeat']

    user = user_repository.find_by_username(session['username'])
    if not user:
        flash('User not found', 'danger')
        return redirect(url_for('password.show'))

    registered_user = User(user['id'], user['username'], user['password'], user['hashcode'])
    if not registered_user.check_password(password):
        flash('Invalid password', 'error')
        return redirect(url_for('login.show'))

    # the given passwords do not match
    if new_password != repeat:
        flash('The given passwords do not match.', 'danger')
        return redirect(url_for('password.show'))

    # change the password
    user_repository.change_password(user['username'], new_password)

    # show the login screen
    flash('Password successfully reset.', 'success')
    return redirect(url_for('login.show'))


