from paprika_connector.connectors.Repository import Repository
from paprika_connector.connectors.Helper import Helper


class RecursiveRepository(Repository):
    def __init__(self, connector):
        Repository.__init__(self, connector)

    def list(self):
        connection = self.get_connection()
        cursor = connection.cursor()

        params = dict()

        statement = "select * from recursives where active=1 order by name"
        statement, parameters = self.statement(statement, params)

        cursor.execute(statement, parameters)
        result = Helper.cursor_to_json(cursor)
        if len(result) == 0:
            return []
        return result
