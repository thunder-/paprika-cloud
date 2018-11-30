from flask import Blueprint
from flask import render_template
from flask import request
from flask import current_app


from paprika_cloud.repositories.DeploymentRepository import DeploymentRepository

deployments = Blueprint('deployments', __name__, template_folder='templates')


@deployments.route('/deployments', methods=['GET'])
def show():
    if request.method == 'GET':
        connector = current_app.connector
        deployment_repository = DeploymentRepository(connector)
        deployments = deployment_repository.list()
        connector.close()
        return render_template('deployments/deployments.html', deployments=deployments)















