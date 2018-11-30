from paprika_connector.connectors.Repository import Repository
from paprika_connector.connectors.Helper import Helper
from datetime import datetime


class ActivationRepository(Repository):
    def __init__(self, connector):
        Repository.__init__(self, connector)

    def insert(self, activation):
        connection = self.get_connection()
        cursor = connection.cursor()

        now = datetime.now()
        connector = self.get_connector()
        ds = connector.get_datasource()

        message = {}
        message['username'] = activation['username']
        message['hashkey'] = activation['hashkey']
        message['created_at'] = now
        message['created_by'] = ds['username']
        message['updated_at'] = now
        message['updated_by'] = ds['username']

        statement = "insert into activations(username, hashkey, created_at, created_by, updated_at, updated_by) values (:username, :hashkey, :created_at, :created_by, :updated_at, :updated_by)"
        statement, parameters = self.statement(statement, message)
        cursor.execute(statement, parameters)
        activation['id'] = cursor.lastrowid
        connection.commit()
        return activation

    def use(self, id):
        connection = self.get_connection()
        cursor = connection.cursor()

        message = {}
        message['id'] = id

        statement = "update activations set active=0, used=1 where id=:id"
        statement, parameters = self.statement(statement, message)
        cursor.execute(statement, parameters)

        connection.commit()

    def find_by_username(self, username):
        connection = self.get_connection()
        cursor = connection.cursor()

        message = {}
        message['username'] = username

        statement = "select * from activations where username=:username and active=1 and used=0"
        statement, parameters = self.statement(statement, message)
        cursor.execute(statement, parameters)
        result = Helper.cursor_to_json(cursor)
        cursor.close()
        if len(result) == 0:
            return None
        return result[0]

    def list_by_username(self, username):
        connection = self.get_connection()
        cursor = connection.cursor()

        message = {}
        message['username'] = username

        statement = "select * from activations where username=:username"
        statement, parameters = self.statement(statement, message)
        cursor.execute(statement, parameters)
        return Helper.cursor_to_json(cursor)

