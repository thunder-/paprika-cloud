from flask import Blueprint
from flask import flash
from flask import request
from flask import redirect
from flask import url_for
from flask import current_app

from paprika_cloud.repositories.DeploymentRepository import DeploymentRepository

deployment_delete = Blueprint('deployment_delete', __name__, template_folder='templates')


@deployment_delete.route('/deployment_delete', methods=['GET'])
def show():
    connector = current_app.connector
    deployment_repository = DeploymentRepository(connector)

    if request.method == 'GET':
        hashcode = request.args.get('hashcode')
        deployment = deployment_repository.find_by_hashcode(hashcode)

        if not deployment:
            flash('Deployment not found.', 'danger')
            return redirect(url_for('hooks.show'))

        deployment_repository.disable(deployment['hashcode'])
        connector.close()
        flash('Deployment deleted.', 'info')
        return redirect(url_for('deployments.show'))















