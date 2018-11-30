from flask import Blueprint, render_template, abort
from flask import Flask, g, flash
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import current_app
import uuid

from paprika_cloud.repositories.FlowRepository import FlowRepository
from paprika_cloud.repositories.ActionRepository import ActionRepository
from paprika_cloud.repositories.ActionGroupRepository import ActionGroupRepository


flow_edit = Blueprint('flow_edit', __name__, template_folder='templates')


@flow_edit.route('/flow_edit', methods=['GET', 'POST'])
def show():
    connector = current_app.connector
    flow_repository = FlowRepository(connector)
    action_repository = ActionRepository(connector)

    hashcode = request.args.get('hashcode')
    flow = flow_repository.find_by_hashcode(hashcode)

    action_group_repository = ActionGroupRepository(connector)
    action_groups = action_group_repository.list_by_tte_id(flow['tte_id'])
    action_groups.extend(action_group_repository.list_by_tte_name('common'))

    for action_group in action_groups:
        actions = action_repository.list_by_agp_id(action_group['id'])
        action_group['actions'] = actions

    if request.method == 'GET':
        flows = flow_repository.list()
        connector.close()
        return render_template('flow_edit/flow_edit.html', flow=flow, flows=flows, action_groups=action_groups)
