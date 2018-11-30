from flask import Blueprint, render_template, abort
from flask import Flask, g, flash
from flask import render_template
from flask import request
from flask import current_app
from flask import redirect
from flask import url_for
import uuid

from paprika_cloud.repositories.UserRepository import UserRepository
from paprika_cloud.repositories.ResetRepository import ResetRepository

password_forgotten = Blueprint('password_forgotten', __name__, template_folder='templates')


@password_forgotten.route('/password_forgotten', methods=['GET', 'POST'])
def show():
    if request.method == 'GET':
        return render_template('password_forgotten/password_forgotten.html')

    connector = current_app.connector
    user_repository = UserRepository(connector)

    username = request.form['username']
    user = user_repository.find_by_username(username)

    if not user:
        connector.close()
        flash('User not found', 'danger')
        return redirect(url_for('password_forgotten.show'))

    # disable all existing reset requests.
    reset_repository = ResetRepository(connector)
    reset_repository.disable(username)

    # create a reset request
    reset = {}
    reset['username'] = username
    reset['hashkey'] = str(uuid.uuid4().hex)
    reset_repository.insert(reset)

    # subject = 'Paprika reset request'
    # message = 'http://localhost:5004/reset?key='+activation['hashkey']
    # Email.send(username, subject, message)

    connector.close()

    flash('A reset e-mail is send to your account.', 'success')
    return redirect(url_for('password_forgotten.show'))
