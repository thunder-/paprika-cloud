from flask import Blueprint, render_template, abort
from flask import Flask, g, flash
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import current_app
import uuid

from paprika_cloud.repositories.FlowRepository import FlowRepository
from flask_login import login_required

flows = Blueprint('flows', __name__, template_folder='templates')


@flows.route('/flows', methods=['GET'])
@login_required
def show():
    if request.method == 'GET':

        connector = current_app.connector

        flow_repository = FlowRepository(connector)
        flows = flow_repository.list()

        connector.close()

        return render_template('flows/flows.html', flows=flows)















