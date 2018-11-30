from flask import Blueprint
from flask import flash
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import current_app
from datetime import datetime
from paprika_cloud.repositories.TriggerRepository import TriggerRepository
from paprika_cloud.repositories.TriggerTypeRepository import TriggerTypeRepository
from paprika_cloud.repositories.RepetitionRepository import RepetitionRepository
import ast

event_create = Blueprint('event_create', __name__, template_folder='templates')


@event_create.route('/event_create', methods=['GET', 'POST'])
def show():
    connector = current_app.connector
    trigger_repository = TriggerRepository(connector)
    repetition_repository = RepetitionRepository(connector)
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
                trigger['intermission'] = 1
                trigger['expected'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if request_type == 'update':
                hashcode = request.args.get('hashcode')
                trigger = trigger_repository.find_by_hashcode(hashcode)
                trigger['type'] = request.args.get('type')

        if not trigger:
            flash('Invalid event', 'danger')
            return redirect(url_for('triggers.show'))

        repetitions = repetition_repository.list()
        connector.close()
        return render_template('event_create/event_create.html', trigger=trigger, repetitions=repetitions)

    trigger = dict()
    trigger['name'] = request.form['name']
    trigger['hashcode'] = request.form['hashcode']
    trigger['description'] = request.form['description']
    trigger['repetition'] = request.form['repetition']
    trigger['intermission'] = request.form['intermission']
    trigger['expected'] = request.form['expected']

    tte_repository = TriggerTypeRepository(connector)
    tte = tte_repository.find_by_name('event')
    trigger['tte_id'] = tte.get('id')

    request_type = request.form['type']
    repetition = repetition_repository.find_by_name(trigger.get('repetition'))
    if not repetition:
        flash('Invalid repetition', 'danger')
        repetitions = repetition_repository.list()
        trigger['type'] = request_type
        return redirect(url_for('event_create.show', trigger=trigger, repetitions=repetitions))

    request_type = request.form['type']
    if request_type == 'create':
        trigger_repository.insert(trigger)
        connector.close()
        flash('Event has been added successfully', 'success')
        return redirect(url_for('triggers.show'))
    if request_type == 'update':
        trigger_repository.update(trigger)
        connector.close()
        flash('Event has been updated successfully', 'success')
        return redirect(url_for('triggers.show'))

    flash('Invalid request_type', 'danger')
    return redirect(url_for('triggers.show'))
