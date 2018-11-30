from paprika_connector.connectors.Repository import Repository
from paprika_connector.connectors.Helper import Helper


class ActionGroupRepository(Repository):
    def __init__(self, connector):
        Repository.__init__(self, connector)

    def list_by_tte_id(self, tte_id):
        connection = self.get_connection()
        cursor = connection.cursor()

        params = {}
        params['tte_id'] = tte_id

        statement = "select * from action_groups where tte_id=:tte_id"
        statement, parameters = self.statement(statement, params)

        cursor.execute(statement, parameters)
        result = Helper.cursor_to_json(cursor)
        if len(result) == 0:
            return []
        return result

    def list_by_tte_name(self, name):
        connection = self.get_connection()
        cursor = connection.cursor()

        params = {}
        params['name'] = name

        statement = "select * from action_groups where tte_id=get_trigger_type_id(:name)"
        statement, parameters = self.statement(statement, params)
        print statement, parameters
        cursor.execute(statement, parameters)
        result = Helper.cursor_to_json(cursor)
        if len(result) == 0:
            return []
        return result
