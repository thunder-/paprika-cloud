import cx_Oracle


class OracleConnector:

    def __init__(self, datasource):
        self.__username = datasource['username']
        self.__password = datasource['password']
        self.__sid = datasource['sid']
        self.__datasource = datasource
        self.__connection = self.connect()

    def get_datasource(self):
        return self.__datasource

    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password

    def get_sid(self):
        return self.__sid

    def get_connection(self):
        return self.__connection

    def set_connection(self, connection):
        self.__connection = connection

    def is_connected(self):
        result = False
        connection = self.get_connection()
        if connection:
            try:
                connection.ping()
                result = True
            except:
                pass
        return result

    def statement(self, statement, message, encoding='utf-8'):
        keys = message.keys()
        target = dict()
        for key in keys:
            if type(message[key]) == unicode:
                target[key] = message[key].encode(encoding)
            else:
                target[key] = message[key]
        return statement, target

    def connect(self):
        username = self.get_username()
        password = self.get_password()
        sid = self.get_sid()
        return cx_Oracle.connect(username + '/' + password + '@' + sid)

    def close(self):
        if self.is_connected():
            connection = self.get_connection()
            connection.close()
