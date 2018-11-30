from flask import Blueprint, render_template, abort
from flask import Flask, g, flash
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import current_app
import uuid

from paprika_cloud.repositories.FlowRepository import FlowRepository
from paprika_cloud.repositories.TriggerTypeRepository import TriggerTypeRepository

flow_create = Blueprint('flow_create', __name__, template_folder='templates')


@flow_create.route('/flow_create', methods=['GET', 'POST'])
def show():
    connector = current_app.connector

    trigger_type_repository = TriggerTypeRepository(connector)
    if request.method == 'GET':
        trigger_types = trigger_type_repository.list()
        connector.close()
        return render_template('flow_create/flow_create.html', trigger_types=trigger_types)

    flow = {}
    flow['name'] = request.form['name']
    flow['description'] = request.form['description']

    tte_hashcode = request.form['trigger_type']
    trigger_type = trigger_type_repository.find_by_hashcode(tte_hashcode)
    flow['tte_id'] = trigger_type.get('id')

    if not trigger_type:
        flash('Invalid trigger type', 'danger')
        return redirect(url_for('flow_create.show'))

    flow_repository = FlowRepository(connector)
    flow_repository.insert(flow)
    connector.close()
    flash('Flow has been added successfully', 'success')
    return redirect(url_for('flows.show'))














