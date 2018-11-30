from paprika_connector.connectors.Repository import Repository
from paprika_connector.connectors.Helper import Helper


class FlowRepository(Repository):
    def __init__(self, connector):
        Repository.__init__(self, connector)

    def list(self):
        connection = self.get_connection()
        cursor = connection.cursor()

        params = {}

        statement = "select flw.*, get_trigger_type(tte_id) as tte from flows flw where active=1 order by id desc"
        statement, parameters = self.statement(statement, params)

        cursor.execute(statement, parameters)
        result = Helper.cursor_to_json(cursor)
        if len(result) == 0:
            return []
        print result
        return result

    def find_by_hashcode(self, hashcode):
        connection = self.get_connection()
        cursor = connection.cursor()

        params = {}
        params['hashcode'] = hashcode

        statement = "select * from flows where hashcode=:hashcode"
        statement, parameters = self.statement(statement, params)

        cursor.execute(statement, parameters)
        result = Helper.cursor_to_json(cursor)
        if len(result) == 0:
            return None
        return result[0]

    def insert(self, flow):
        connection = self.get_connection()
        cursor = connection.cursor()

        params = {}
        params['name'] = flow['name']
        params['description'] = flow['description']
        params['tte_id'] = flow['tte_id']

        statement = "insert into flows(name, description, tte_id) values (:name, :description, :tte_id)"

        # '{"nodes": [ {"id":"1000", "name":"start", "type":"start", "label":"&#xf111;", "x":"300", "y":"250", "out":"1001"}, {"id":"1002", "name":"end", "type":"end", "label":"&#xf111;", "x":"700", "y":"300", "in":"1001"} ]}'
        statement, parameters = self.statement(statement, params)
        cursor.execute(statement, parameters)
        flow['id'] = cursor.lastrowid
        connection.commit()
        return flow

    def disable(self, hashcode):
        connection = self.get_connection()
        cursor = connection.cursor()

        params = {}
        params['hashcode'] = hashcode

        statement = "update flows set active=0 where hashcode=:hashcode"
        statement, parameters = self.statement(statement, params)
        cursor.execute(statement, parameters)
        connection.commit()

    def delete(self, flow):
        connection = self.get_connection()
        cursor = connection.cursor()

        message = {}

        message['hashcode'] = flow['hashcode']

        statement = "delete from flows where hashcode=:hashcode"
        statement, parameters = self.statement(statement, message)
        cursor.execute(statement, parameters)
        connection.commit()

    def update(self, flow):
        connection = self.get_connection()
        cursor = connection.cursor()

        message = {}
        message['name'] = flow['name']
        message['payload'] = flow['payload']
        message['hashcode'] = flow['hashcode']

        statement = "update flows set name=:name, payload=:payload where hashcode=:hashcode"
        statement, parameters = self.statement(statement, message)
        cursor.execute(statement, parameters)
        connection.commit()

    def reset(self, flow):
        connection = self.get_connection()
        cursor = connection.cursor()

        message = {}
        message['payload'] = flow['payload']
        message['hashcode'] = flow['hashcode']

        statement = "delete from flows payload=:payload where hashcode=:hashcode"
        statement, parameters = self.statement(statement, message)
        cursor.execute(statement, parameters)
        connection.commit()

    def update_name(self, flow):
        connection = self.get_connection()
        cursor = connection.cursor()

        message = {}
        message['name'] = flow['name']
        message['description'] = flow['description']
        message['hashcode'] = flow['hashcode']

        statement = "update flows set name=:name, description=:description where hashcode=:hashcode"
        statement, parameters = self.statement(statement, message)
        cursor.execute(statement, parameters)
        connection.commit()

    def update_node_name(self, flow):
        connection = self.get_connection()
        cursor = connection.cursor()

        message = {}
        message['name'] = flow['name']
        message['payload'] = flow['payload']
        message['hashcode'] = flow['hashcode']

        statement = "update flows set name=:name where hashcode=:hashcode and payload:=payload"
        statement, parameters = self.statement(statement, message)
        cursor.execute(statement, parameters)
        connection.commit()
