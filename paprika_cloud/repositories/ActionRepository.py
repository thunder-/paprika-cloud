from paprika_connector.connectors.Repository import Repository
from paprika_connector.connectors.Helper import Helper


class ActionRepository(Repository):
    def __init__(self, connector):
        Repository.__init__(self, connector)

    def list_by_agp_id(self, agp_id):
        connection = self.get_connection()
        cursor = connection.cursor()

        params = dict()
        params['agp_id'] = agp_id

        statement = "select * from actions where agp_id=:agp_id"
        statement, parameters = self.statement(statement, params)

        cursor.execute(statement, parameters)
        result = Helper.cursor_to_json(cursor)
        if len(result) == 0:
            return []
        return result

    def list_groupnames(self):
        connection = self.get_connection()
        cursor = connection.cursor()

        params = {}

        statement = "select groupname, icon from actions group by groupname,icon"
        statement, parameters = self.statement(statement, params)

        cursor.execute(statement, parameters)
        result = Helper.cursor_to_json(cursor)
        if len(result) == 0:
            return []
        return result

    def list_by_groupname(self, groupname, icon):
        connection = self.get_connection()
        cursor = connection.cursor()

        params = {}
        params['groupname'] = groupname
        params['icon'] = icon

        statement = "select * from actions where groupname=:groupname and icon=:icon"
        statement, parameters = self.statement(statement, params)

        cursor.execute(statement, parameters)
        result = Helper.cursor_to_json(cursor)
        if len(result) == 0:
            return []
        return result

    def list(self):
        connection = self.get_connection()
        cursor = connection.cursor()

        params = {}

        statement = "select * from actions"
        statement, parameters = self.statement(statement, params)

        cursor.execute(statement, parameters)
        result = Helper.cursor_to_json(cursor)
        if len(result) == 0:
            return []
        return result

    def find_by_name(self, name):
        connection = self.get_connection()
        cursor = connection.cursor()

        params = {}
        params['name'] = name

        statement = "select * from actions where name=:name"
        statement, parameters = self.statement(statement, params)

        cursor.execute(statement, parameters)
        result = Helper.cursor_to_json(cursor)
        if len(result) == 0:
            return None
        return result[0]

    def find_by_color(self, color):
        connection = self.get_connection()
        cursor = connection.cursor()

        params = {}
        params['color'] = color

        statement = "select * from actions where color=:color"
        statement, parameters = self.statement(statement, params)

        cursor.execute(statement, parameters)
        result = Helper.cursor_to_json(cursor)
        if len(result) == 0:
            return None
        return result[0]

    def find_by_icon(self, icon):
        connection = self.get_connection()
        cursor = connection.cursor()

        params = {}
        params['icon'] = icon

        statement = "select * from actions where icon=:icon"
        statement, parameters = self.statement(statement, params)

        cursor.execute(statement, parameters)
        result = Helper.cursor_to_json(cursor)
        if len(result) == 0:
            return None
        return result[0]
