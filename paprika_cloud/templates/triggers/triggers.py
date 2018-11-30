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
from paprika_cloud.repositories.TriggerRepository import TriggerRepository

triggers = Blueprint('triggers', __name__, template_folder='templates')


@triggers.route('/triggers', methods=['GET'])
@login_required
def show():
    connector = current_app.connector
    trigger_repository = TriggerRepository(connector)
    triggers = trigger_repository.list()
    return render_template('triggers/triggers.html', triggers=triggers)





