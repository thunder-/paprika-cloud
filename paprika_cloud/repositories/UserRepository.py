import hashlib
from paprika_connector.connectors.Repository import Repository
from paprika_connector.connectors.Helper import Helper
from paprika_cloud.repositories.SessionRepository import SessionRepository


class UserRepository(Repository):
    def __init__(self, connector):
        Repository.__init__(self, connector)

    def find_by_id(self, id):
        connection = self.get_connection()
        cursor = connection.cursor()

        m = {}
        m['id'] = id

        statement = "select * from users where id=:id"
        statement, parameters = self.statement(statement, m)
        cursor.execute(statement, parameters)
        result = Helper.cursor_to_json(cursor)
        cursor.close()
        if len(result) == 0:
            return None
        return result[0]

    def find_by_username(self, username):
        connection = self.get_connection()
        cursor = connection.cursor()

        m = {}
        m['username'] = username

        statement = "select * from users where username=:username and active=1"
        statement, parameters = self.statement(statement, m)
        cursor.execute(statement, parameters)
        result = Helper.cursor_to_json(cursor)
        cursor.close()
        if len(result) == 0:
            return None
        return result[0]

    def find_all_by_username(self, username):
        connection = self.get_connection()
        cursor = connection.cursor()

        m = {}
        m['username'] = username

        statement = "select * from users where username=:username"
        statement, parameters = self.statement(statement, m)
        cursor.execute(statement, parameters)
        result = Helper.cursor_to_json(cursor)
        cursor.close()
        if len(result) == 0:
            return None
        return result[0]

    def insert(self, user):
        connection = self.get_connection()
        cursor = connection.cursor()

        sha512 = hashlib.sha512()
        sha512.update(user['password'])
        password = sha512.hexdigest()

        message = {}
        message['username'] = user['username']
        message['password'] = password
        message['active'] = user['active']

        statement = "insert into users(username, password, active) values (:username, :password, :active)"
        statement, parameters = self.statement(statement, message)
        cursor.execute(statement, parameters)
        user['id'] = cursor.lastrowid
        connection.commit()
        return user

    def update(self, user):
        connection = self.get_connection()
        cursor = connection.cursor()

        m = {}
        m['name'] = user['name']
        m['nickname'] = user['nickname']
        m['hashcode'] = user['hashcode']
        m['organization'] = user['organization']

        statement = "update users set name=:name, nickname=:nickname, organization=:organization where hashcode=:hashcode"
        statement, parameters = self.statement(statement, m)
        cursor.execute(statement, parameters)

        connection.commit()
        return user

    def register(self, username, password):
        user = self.find_by_username(username)
        if not user:
            self.insert({"username": username, "password": password})

    def login(self, username, password):
        user = self.find_by_username(username)
        sha512 = hashlib.sha512()
        sha512.update(password)

        if user:
            if user['password'] == sha512.hexdigest():
                session_repository = SessionRepository(self.get_connector())
                session = session_repository.create()
                session = session_repository.find_by_id(session['id'])
                return session['hashcode']
        return None

    def list(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("select * from users")
        return Helper.cursor_to_json(cursor)

    def find_by_hashcode(self, hashcode):
        connection = self.get_connection()
        cursor = connection.cursor()

        m = {}
        m['hashcode'] = hashcode

        statement = "select * from users where hashcode=:hashcode"
        statement, parameters = self.statement(statement, m)
        cursor.execute(statement, parameters)
        result = Helper.cursor_to_json(cursor)
        cursor.close()
        if len(result) == 0:
            return None
        return result[0]

    def activate(self, username):
        connection = self.get_connection()
        cursor = connection.cursor()

        message = {}
        message['username'] = username

        statement = "update users set active=1 where username=:username"
        statement, parameters = self.statement(statement, message)
        cursor.execute(statement, parameters)

        connection.commit()

    def change_password(self, username, password):
        connection = self.get_connection()
        cursor = connection.cursor()

        sha512 = hashlib.sha512()
        sha512.update(password)
        password = sha512.hexdigest()

        message = {}
        message['username'] = username
        message['password'] = password

        statement = "update users set password=:password where username=:username"
        statement, parameters = self.statement(statement, message)
        cursor.execute(statement, parameters)

        connection.commit()