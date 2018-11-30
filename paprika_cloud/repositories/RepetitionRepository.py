from paprika_connector.connectors.Repository import Repository
from paprika_connector.connectors.Helper import Helper


class RepetitionRepository(Repository):
    def __init__(self, connector):
        Repository.__init__(self, connector)

    def list(self):
        connection = self.get_connection()
        cursor = connection.cursor()

        params = dict()

        statement = "select * from repetitions where active=1 order by name"
        statement, parameters = self.statement(statement, params)

        cursor.execute(statement, parameters)
        result = Helper.cursor_to_json(cursor)
        if len(result) == 0:
            return []
        return result

    def find_by_name(self, name):
        connection = self.get_connection()
        cursor = connection.cursor()

        params = dict()
        params['name'] = name

        statement = "select * from repetitions where name=:name and active=1"
        statement, parameters = self.statement(statement, params)

        cursor.execute(statement, parameters)
        result = Helper.cursor_to_json(cursor)
        if len(result) == 0:
            return None
        return result[0]
