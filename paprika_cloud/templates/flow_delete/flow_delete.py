from flask import Blueprint, render_template, abort
from flask import Flask, g, flash
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import current_app
import uuid

from paprika_cloud.repositories.FlowRepository import FlowRepository


flow_delete = Blueprint('flow_delete', __name__, template_folder='templates')


@flow_delete.route('/flow_delete', methods=['GET'])
def show():
    connector = current_app.connector
    flow_repository = FlowRepository(connector)

    if request.method == 'GET':
        hashcode = request.args.get('hashcode')
        flow = flow_repository.find_by_hashcode(hashcode)

        if not flow:
            flash('Flow not found.', 'danger')
            return redirect(url_for('flows.show'))

        flow_repository.disable(flow['hashcode'])
        connector.close()
        flash('Flow deleted.', 'info')
        return redirect(url_for('flows.show'))















