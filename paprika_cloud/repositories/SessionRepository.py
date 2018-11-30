from paprika_connector.connectors.Repository import Repository
from paprika_connector.connectors.Helper import Helper


class SessionRepository(Repository):
    def __init__(self, connector):
        Repository.__init__(self, connector)

    def create(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        statement = "insert into sessions () values ()"
        cursor.execute(statement)
        session = {}
        session['id'] = cursor.lastrowid
        connection.commit()
        return session

    def find_by_id(self, id):
        connection = self.get_connection()
        cursor = connection.cursor()

        m = {}
        m['id'] = id

        statement = "select * from sessions where id=:id"
        statement, parameters = self.statement(statement, m)
        print statement, parameters
        cursor.execute(statement, parameters)
        result = Helper.cursor_to_json(cursor)
        cursor.close()
        if len(result) == 0:
            return None
        return result[0]

    def find_by_hashcode(self, hashcode):
        connection = self.get_connection()
        cursor = connection.cursor()

        m = {}
        m['hashcode'] = hashcode

        statement = "select * from sessions where hashcode=:hashcode"
        statement, parameters = self.statement(statement, m)
        cursor.execute(statement, parameters)
        result = Helper.cursor_to_json(cursor)
        cursor.close()
        if len(result) == 0:
            return None
        return result[0]
