from flask import Blueprint, render_template, abort
from flask import Flask, g, flash
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import current_app
import uuid
import ast
from paprika_cloud.repositories.TriggerRepository import TriggerRepository
from paprika_cloud.repositories.DatasourceRepository import DatasourceRepository
from paprika_cloud.repositories.TriggerTypeRepository import TriggerTypeRepository

hook_create = Blueprint('hook_create', __name__, template_folder='templates')


@hook_create.route('/hook_create', methods=['GET', 'POST'])
def show():
    connector = current_app.connector
    trigger_repository = TriggerRepository(connector)
    datasource_repository = DatasourceRepository(connector)
    if request.method == 'GET':
        request_type = request.args.get('type')

        trigger = request.args.get('trigger')
        if trigger:
            trigger = ast.literal_eval(trigger)

        if not trigger:
            if request_type == 'create':
                trigger = dict()
                trigger['type'] = request.args.get('type')
                trigger['hashcode'] = request.args.get('hashcode')
            if request_type == 'update':
                hashcode = request.args.get('hashcode')
                trigger = trigger_repository.find_by_hashcode(hashcode)
                trigger['type'] = request.args.get('type')

        if not trigger:
            flash('Invalid hook', 'danger')
            return redirect(url_for('triggers.show'))

        datasources = datasource_repository.list()
        connector.close()
        return render_template('hook_create/hook_create.html', trigger=trigger, datasources=datasources)

    trigger = dict()
    trigger['name'] = request.form['name']
    trigger['hashcode'] = request.form['hashcode']
    trigger['description'] = request.form['description']
    trigger['datasource'] = request.form['datasource']
    trigger['selector'] = request.form['selector']
    trigger['updater'] = request.form['updater']
    trigger['options'] = request.form['options']

    tte_repository = TriggerTypeRepository(connector)
    tte = tte_repository.find_by_name('hook')
    trigger['tte_id'] = tte.get('id')

    request_type = request.form['type']
    datasource = datasource_repository.find_by_name(trigger.get('datasource'))
    if not datasource:
        flash('Invalid datasource', 'danger')
        datasources = datasource_repository.list()
        trigger['type'] = request_type
        return redirect(url_for('hook_create.show', trigger=trigger, datasources=datasources))

    if request_type == 'create':
        trigger_repository.insert(trigger)
        connector.close()
        flash('Hook has been added successfully', 'success')
        return redirect(url_for('triggers.show'))
    if request_type == 'update':
        trigger_repository.update(trigger)
        connector.close()
        flash('Hook has been updated successfully', 'success')
        return redirect(url_for('triggers.show'))

    flash('Invalid request_type', 'danger')
    return redirect(url_for('triggers.show'))
