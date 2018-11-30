from flask import Blueprint, render_template, abort
from flask import Flask, g, flash
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import current_app
import uuid

from paprika_cloud.repositories.ActivationRepository import ActivationRepository
from paprika_cloud.repositories.UserRepository import UserRepository


register = Blueprint('register', __name__, template_folder='templates')


@register.route('/register', methods=['GET', 'POST'])
def show():
    if request.method == 'GET':
        return render_template('register/register.html')

    connector = current_app.connector
    user_repository = UserRepository(connector)

    username = request.form['username']
    password = request.form['password']
    user = user_repository.find_all_by_username(username)
    if user:
        connector.close()
        flash('User already registered', 'danger')
        return redirect(url_for('register.show'))

    user = {}
    user['username'] = username
    user['password'] = password
    user['active'] = 0
    user = user_repository.insert(user)

    # create an activation request
    activation = {}
    activation['username'] = username
    activation['hashkey'] = str(uuid.uuid4().hex)
    activation_repository = ActivationRepository(connector)
    activation_repository.insert(activation)

    # subject = 'Paprika activation request'
    # message = 'http://localhost:5004/activate?key='+activation['hashkey']
    # Email.send(username, subject, message)

    connector.close()

    flash('User successfully registered, an activation e-mail is send to your account.', 'success')
    return redirect(url_for('register.show'))


