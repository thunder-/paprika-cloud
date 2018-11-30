from flask_restful import Resource
from flask import request
import json
from flask import current_app
from paprika_cloud.repositories.FlowRepository import FlowRepository


class ResetFlow(Resource):
    def post(self):
        try:
            content = request.get_json(silent=True)
            payload = dict()
            payload['nodes'] = content['nodes']
            payload = json.dumps(payload)

            connector = current_app.connector
            hashcode = content.get('hashcode')
            flow_repository = FlowRepository(connector)
            flow = flow_repository.find_by_hashcode(hashcode)
            if flow:
                flow['payload'] = []
                flow_repository.update(flow)
            connector.close()
            return {"hashcode": hashcode}
        except:
            return {}

