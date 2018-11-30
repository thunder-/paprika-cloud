from flask import Blueprint, render_template, abort
from flask import Flask, g, flash
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import current_app
import uuid

from paprika_cloud.repositories.ResetRepository import ResetRepository
from paprika_cloud.repositories.UserRepository import UserRepository


reset = Blueprint('reset', __name__, template_folder='templates')


@reset.route('/reset', methods=['GET', 'POST'])
def show():
    if request.method == 'GET':
        key = request.args.get('key')
        return render_template('reset/reset.html', key=key)

    connector = current_app.connector

    password = request.form['password']
    repeat = request.form['repeat']
    hashkey = request.form['hashkey']

    reset_repository = ResetRepository(connector)
    reset_request = reset_repository.find_by_hashkey(hashkey)

    if not reset_request:
        print "reset not found"
        flash('Invalid reset request.', 'danger')
        return redirect(url_for('reset.show', key=hashkey))

    username = reset_request['username']
    user_repository = UserRepository(connector)
    user = user_repository.find_by_username(username)

    # the given user is not found
    if not user:
        print "user not found"
        flash('Invalid reset request.', 'danger')
        return redirect(url_for('reset.show', key=hashkey))

    # the given passwords do not match
    if password != repeat:
        flash('The given passwords do not match.','danger')
        return redirect(url_for('reset.show', key=hashkey))

    # enable the user
    user_repository.change_password(username, password)

    # mark the reset request as used.
    reset_repository.use(reset_request['id'])

    # show the login screen
    flash('Password successfully reset.', 'success')
    return redirect(url_for('login.show'))


