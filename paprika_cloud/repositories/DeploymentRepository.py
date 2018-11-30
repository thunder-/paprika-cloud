from paprika_connector.connectors.Repository import Repository
from paprika_connector.connectors.Helper import Helper
from datetime import datetime

class DeploymentRepository(Repository):
    def __init__(self, connector):
        Repository.__init__(self, connector)

    def list(self):
        connection = self.get_connection()
        cursor = connection.cursor()

        params = {}

        statement = "select dpt.*, get_trigger_trigger_type(tgr_id) as tte from deployments dpt where active=1 order by id desc"
        statement, parameters = self.statement(statement, params)

        cursor.execute(statement, parameters)
        result = Helper.cursor_to_json(cursor)
        if len(result) == 0:
            return []
        return result

    def find_by_hashcode(self, hashcode):
        connection = self.get_connection()
        cursor = connection.cursor()

        params = {}
        params['hashcode'] = hashcode

        statement = "select * from deployments where hashcode=:hashcode"
        statement, parameters = self.statement(statement, params)

        cursor.execute(statement, parameters)
        result = Helper.cursor_to_json(cursor)
        if len(result) == 0:
            return None
        return result[0]

    def insert(self, deployment):
        connection = self.get_connection()
        cursor = connection.cursor()

        now = datetime.now()
        connector = self.get_connector()
        ds = connector.get_datasource()

        params = {}
        params['name'] = deployment.get('name')
        params['pattern'] = deployment.get('pattern', None)
        params['tgr_id'] = deployment.get('tgr_id')
        params['flw_id'] = deployment.get('flw_id')
        params['e_flw_id'] = deployment.get('e_flw_id', None)
        params['created_at'] = now
        params['created_by'] = ds['username']
        params['updated_at'] = now
        params['updated_by'] = ds['username']

        statement = "insert into deployments(name, pattern, tgr_id, flw_id, e_flw_id, created_at, created_by, updated_at, updated_by) values (:name, :pattern, :tgr_id, :flw_id, :e_flw_id, :created_at, :created_by, :updated_at, :updated_by)"
        statement, parameters = self.statement(statement, params)
        print statement, parameters
        cursor.execute(statement, parameters)
        deployment['id'] = cursor.lastrowid
        connection.commit()
        return deployment

    def disable(self, hashcode):
        connection = self.get_connection()
        cursor = connection.cursor()

        params = {}
        params['hashcode'] = hashcode

        statement = "update deployments set active=0 where hashcode=:hashcode"
        statement, parameters = self.statement(statement, params)
        cursor.execute(statement, parameters)
        connection.commit()

    def update(self, deployment):
        connection = self.get_connection()
        cursor = connection.cursor()

        now = datetime.now()
        connector = self.get_connector()
        ds = connector.get_datasource()

        params = {}
        params['hashcode'] = deployment.get('hashcode')
        params['name'] = deployment.get('name')
        params['pattern'] = deployment.get('pattern', None)
        params['tgr_id'] = deployment.get('tgr_id')
        params['flw_id'] = deployment.get('flw_id')
        params['e_flw_id'] = deployment.get('e_flw_id', None)
        params['updated_at'] = now
        params['updated_by'] = ds['username']

        statement = "update deployments set name=:name, pattern=:pattern, tgr_id=:tgr_id, flw_id=:flw_id, e_flw_id=:e_flw_id, updated_at=:updated_at, updated_by=:updated_by where hashcode=:hashcode"
        statement, parameters = self.statement(statement, params)
        cursor.execute(statement, parameters)
        connection.commit()

