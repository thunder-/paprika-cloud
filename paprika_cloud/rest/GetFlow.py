from flask_restful import Resource
from flask import request
from flask import current_app
from paprika_cloud.repositories.FlowRepository import FlowRepository


class GetFlow(Resource):
    def get(self):
        try:
            hashcode = request.args.get('hashcode')
            connector = current_app.connector

            flow_repository = FlowRepository(connector)
            flow = flow_repository.find_by_hashcode(hashcode)
            connector.close()

            return flow
        except:
            return {}

