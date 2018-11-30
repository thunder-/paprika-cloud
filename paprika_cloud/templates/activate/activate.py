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


activate = Blueprint('activate', __name__, template_folder='templates')


@activate.route('/activate', methods=['GET', 'POST'])
def show():
    if request.method == 'GET':
        key = request.args.get('key')
        return render_template('activate/activate.html', key=key)

    connector = current_app.connector

    username = request.form['username']
    hashkey = request.form['hashkey']

    user_repository = UserRepository(connector)
    user = user_repository.find_all_by_username(username)

    # the given user is not found
    if not user:
        print "user not found"
        flash('Invalid activation request.', 'danger')
        return redirect(url_for('activate.show', key=hashkey))

    activation_repository = ActivationRepository(connector)
    activation = activation_repository.find_by_username(username)

    # there was no activation found for the give user.
    if not activation:
        print "activation not found"
        flash('Invalid activation request.', 'danger')
        return redirect(url_for('activate.show', key=hashkey))

    # the given hashkey does not match with activation request
    if activation['hashkey'] != hashkey:
        print "invalid hashkey"
        flash('Invalid activation request.', 'danger')
        return redirect(url_for('activate.show', key=hashkey))

    # enable the user
    user_repository.activate(username)

    # mark the activation as used.
    activation_repository.use(activation['id'])

    # show the login screen
    flash('User successfully activated.', 'success')
    print "active.show, going to redirect"
    return redirect(url_for('login.show'))


