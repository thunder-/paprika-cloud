from flask import Blueprint, render_template, abort
from flask import Flask, g, flash
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import current_app
import uuid

from paprika_cloud.repositories.TriggerRepository import TriggerRepository
from paprika_cloud.repositories.FlowRepository import FlowRepository
from paprika_cloud.repositories.DeploymentRepository import DeploymentRepository
deployment_create = Blueprint('deployment_create', __name__, template_folder='templates')


@deployment_create.route('/deployment_create', methods=['GET', 'POST'])
def show():
    connector = current_app.connector

    deployment_repository = DeploymentRepository(connector)
    trigger_repository = TriggerRepository(connector)
    flow_repository = FlowRepository(connector)
    if request.method == 'GET':
        deployment = None
        request_type = request.args.get('type')
        if request_type == 'create':
            deployment = dict()
            deployment['type'] = request.args.get('type')
            deployment['hashcode'] = request.args.get('hashcode')
        if request_type == 'update':
            hashcode = request.args.get('hashcode')
            deployment = deployment_repository.find_by_hashcode(hashcode)
            deployment['type'] = request.args.get('type')

        if not deployment:
            flash('Invalid deployment', 'danger')
            return redirect(url_for('deployments.show'))

        triggers = trigger_repository.list()
        flows = flow_repository.list()
        connector.close()
        return render_template('deployment_create/deployment_create.html', deployment=deployment, triggers=triggers, flows=flows)

    deployment = dict()
    deployment['name'] = request.form['name']
    deployment['hashcode'] = request.form['hashcode']
    deployment['pattern'] = request.form['pattern']
    deployment['tgr_id'] = request.form['tgr_id']
    deployment['flw_id'] = request.form['flw_id']
    deployment['e_flw_id'] = request.form['e_flw_id']

    request_type = request.form['type']
    if request_type == 'create':
        deployment_repository.insert(deployment)
        connector.close()
        flash('Deployment has been added successfully', 'success')
        return redirect(url_for('deployments.show'))
    if request_type == 'update':
        deployment_repository.update(deployment)
        connector.close()
        flash('Deployment has been updated successfully', 'success')
        return redirect(url_for('deployments.show'))

    flash('Invalid request_type', 'danger')
    return redirect(url_for('deployments.show'))
