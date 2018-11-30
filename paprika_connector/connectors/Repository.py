from paprika_connector.connectors.Helper import Helper

class Repository(object):

    def __init__(self, connector):
        object.__init__(self)
        self.__connector = connector
        self.__sequence = None

    def get_sequence(self):
        return self.__sequence

    def set_sequence(self, sequence):
        self.__sequence = sequence

    def nextval(self):
        sequence = self.get_sequence()

        if sequence:
            connection = self.get_connection()
            cursor = connection.cursor()

            params = dict()

            statement = "select " + sequence + ".nextval from dual"
            statement, parameters = self.statement(statement, params)

            cursor.execute(statement, parameters)
            result = Helper.cursor_to_json(cursor)
            if len(result) == 0:
                return None
            return result[0].get('nextval')

        return None

    def get_connector(self):
        return self.__connector

    def get_connection(self):
        connector = self.get_connector()
        connection = connector.get_connection()
        if not connector.is_connected():
            connection = connector.connect()
            connector.set_connection(connection)
        return connection

    def statement(self, statement, message, encoding='utf-8'):
        connector = self.get_connector()
        return connector.statement(statement, message, encoding)

    def has_lastrowid(self):
        connector = self.get_connector()
        datasource = connector.get_datasource()
        if datasource['type'] == 'oracle':
            return False
        return True
