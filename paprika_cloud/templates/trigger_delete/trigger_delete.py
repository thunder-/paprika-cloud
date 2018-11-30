from flask import Blueprint, render_template, abort
from flask import Flask, g, flash
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import current_app

from paprika_cloud.repositories.TriggerRepository import TriggerRepository

trigger_delete = Blueprint('trigger_delete', __name__, template_folder='templates')


@trigger_delete.route('/trigger_delete', methods=['GET'])
def show():
    connector = current_app.connector
    trigger_repository = TriggerRepository(connector)

    if request.method == 'GET':
        hashcode = request.args.get('hashcode')
        trigger = trigger_repository.find_by_hashcode(hashcode)

        if not trigger:
            flash('Trigger not found.', 'danger')
            return redirect(url_for('triggers.show'))

        trigger_repository.disable(trigger['hashcode'])
        connector.close()
        flash('Trigger deleted.', 'info')
        return redirect(url_for('triggers.show'))















