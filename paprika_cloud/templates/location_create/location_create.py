from flask import Blueprint
from flask import flash
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import current_app
from paprika_cloud.repositories.TriggerRepository import TriggerRepository
from paprika_cloud.repositories.TriggerTypeRepository import TriggerTypeRepository
from paprika_cloud.repositories.RecursiveRepository import RecursiveRepository
import ast

location_create = Blueprint('location_create', __name__, template_folder='templates')


@location_create.route('/location_create', methods=['GET', 'POST'])
def show():
    connector = current_app.connector
    trigger_repository = TriggerRepository(connector)
    recursive_repository = RecursiveRepository(connector)
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
                trigger['depth'] = -1
            if request_type == 'update':
                hashcode = request.args.get('hashcode')
                trigger = trigger_repository.find_by_hashcode(hashcode)
                trigger['type'] = request.args.get('type')

        if not trigger:
            flash('Invalid location', 'danger')
            return redirect(url_for('triggers.show'))

        recursives = recursive_repository.list()
        connector.close()
        return render_template('location_create/location_create.html', trigger=trigger, recursives=recursives)

    trigger = dict()
    trigger['name'] = request.form['name']
    trigger['hashcode'] = request.form['hashcode']
    trigger['description'] = request.form['description']
    trigger['url'] = request.form['url']
    trigger['patterns'] = request.form['patterns']
    trigger['recursive'] = request.form['recursive']
    trigger['depth'] = request.form['depth']

    tte_repository = TriggerTypeRepository(connector)
    tte = tte_repository.find_by_name('location')
    trigger['tte_id'] = tte.get('id')

    request_type = request.form['type']

    if not trigger['depth'] and trigger['recursive'] == '1':
        flash('depth is required', 'danger')
        recursives = recursive_repository.list()
        trigger['type'] = request_type
        return redirect(url_for('location_create.show', trigger=trigger, recursives=recursives))

    request_type = request.form['type']
    if request_type == 'create':
        trigger_repository.insert(trigger)
        connector.close()
        flash('Location has been added successfully', 'success')
        return redirect(url_for('triggers.show'))
    if request_type == 'update':
        trigger_repository.update(trigger)
        connector.close()
        flash('Location has been updated successfully', 'success')
        return redirect(url_for('triggers.show'))

    flash('Invalid request_type', 'danger')
    return redirect(url_for('triggers.show'))
