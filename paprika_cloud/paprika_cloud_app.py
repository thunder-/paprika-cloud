from flask import Flask, g, flash
from flask_restful import Api
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session

from paprika_connector.connectors.DatasourceBuilder import DatasourceBuilder
from paprika_connector.connectors.ConnectorFactory import ConnectorFactory
from paprika_cloud.repositories.UserRepository import UserRepository
from paprika_cloud.repositories.ActivationRepository import ActivationRepository
from paprika_cloud.system.Email import Email

from datetime import date

from paprika_cloud.rest.GetFlow import GetFlow
from paprika_cloud.rest.SaveFlow import SaveFlow
from paprika_cloud.rest.ResetFlow import ResetFlow

from paprika_cloud.templates.index.index import index
from paprika_cloud.templates.login.login import login
from paprika_cloud.templates.register.register import register
from paprika_cloud.templates.password_forgotten.password_forgotten import password_forgotten
from paprika_cloud.templates.reset.reset import reset
from paprika_cloud.templates.activate.activate import activate
from paprika_cloud.templates.profile.profile import profile
from paprika_cloud.templates.password.password import password
from paprika_cloud.templates.flows.flows import flows
from paprika_cloud.templates.flow_create.flow_create import flow_create
from paprika_cloud.templates.flow_edit.flow_edit import flow_edit
from paprika_cloud.templates.flow_delete.flow_delete import flow_delete
from paprika_cloud.templates.triggers.triggers import triggers
from paprika_cloud.templates.trigger_delete.trigger_delete import trigger_delete
from paprika_cloud.templates.hook_create.hook_create import hook_create
from paprika_cloud.templates.event_create.event_create import event_create
from paprika_cloud.templates.location_create.location_create import location_create
from paprika_cloud.templates.stream_create.stream_create import stream_create
from paprika_cloud.templates.deployments.deployments import deployments
from paprika_cloud.templates.deployment_create.deployment_create import deployment_create
from paprika_cloud.templates.deployment_delete.deployment_delete import deployment_delete


from paprika_cloud.templates.login.User import User

from flask_login import LoginManager
from flask_login import login_user, logout_user, current_user, login_required
from flask_login import UserMixin
import hashlib
import argparse
import paprika_cloud
import os
import uuid


app = Flask(__name__)
app.secret_key = 'super secret key'
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login.show'
paprika_ds = DatasourceBuilder.build('paprika_cloud-ds.json', os.path.dirname(paprika_cloud.__file__))
connector = ConnectorFactory.create_connector(paprika_ds)

app.connector = connector

api.add_resource(GetFlow, '/rest/get_flow')
api.add_resource(SaveFlow, '/rest/save_flow')
api.add_resource(ResetFlow, '/rest/reset_flow')


app.register_blueprint(index)
app.register_blueprint(login)
app.register_blueprint(register)
app.register_blueprint(activate)
app.register_blueprint(password_forgotten)
app.register_blueprint(reset)
app.register_blueprint(profile)
app.register_blueprint(password)
app.register_blueprint(flows)
app.register_blueprint(flow_create)
app.register_blueprint(flow_edit)
app.register_blueprint(flow_delete)
app.register_blueprint(triggers)
app.register_blueprint(trigger_delete)
app.register_blueprint(hook_create)
app.register_blueprint(event_create)
app.register_blueprint(location_create)
app.register_blueprint(stream_create)
app.register_blueprint(deployments)
app.register_blueprint(deployment_create)
app.register_blueprint(deployment_delete)


@login_manager.user_loader
def load_user(user_id):
    user_repository = UserRepository(connector)
    user = user_repository.find_by_id(user_id)
    connector.close()
    return User(user['id'], user['username'], user['password'], user['hashcode'])


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login.show'))


@app.before_request
def before_request():
    g.user = current_user


def main(args=None):
    # Instantiate the parser
    parser = argparse.ArgumentParser(description="paprika cloud server")
    parser.add_argument('-v', action='store_true', help='show the version')
    parser.add_argument('-d', action='store_true', help='debug mode')
    parser.add_argument('-b', type=str, default='127.0.0.1', help='host')
    parser.add_argument('-p', type=int, default='5004', help='port')
    args = parser.parse_args(args)

    if args.v:
        print "version " + paprika_cloud.__version__
        exit(0)

    debug = False
    if args.d:
        debug = True

    host = None
    if args.b:
        host = args.b

    port = None
    if args.p:
        port = args.p

    app.secret_key = 'paprika cloud super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=debug, port=port, host=host)


if __name__ == '__main__':
    main(args=None)


