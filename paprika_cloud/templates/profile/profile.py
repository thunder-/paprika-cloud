from flask import Blueprint, render_template, abort
from flask import Flask, g, flash
from flask import render_template
from flask import request
from flask import current_app
from flask import redirect
from flask import url_for
from flask import session
from flask_login import login_required
import uuid

from paprika_cloud.repositories.UserRepository import UserRepository
from paprika_cloud.repositories.ResetRepository import ResetRepository
from paprika_cloud.system.DictExt import DictExt

profile = Blueprint('profile', __name__, template_folder='templates')


@profile.route('/profile', methods=['GET', 'POST'])
@login_required
def show():
    connector = current_app.connector
    user_repository = UserRepository(connector)

    if request.method == 'GET':
        hashcode = request.args.get('hashcode')
        user = user_repository.find_by_hashcode(hashcode)
        user = DictExt.strip_none(user)
        connector.close()
        return render_template('profile/profile.html', user=user)

    user = {}
    user['hashcode'] = request.form['hashcode']
    user['name'] = request.form['name']
    user['nickname'] = request.form['nickname']
    user['organization'] = request.form['organization']
    print user
    user_repository.update(user)
    user = user_repository.find_by_hashcode(user['hashcode'])

    flash('User has been updated', 'info')
    return render_template('profile/profile.html', user=user)



