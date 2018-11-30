from flask_login import UserMixin
import hashlib


class User(UserMixin):
    def __init__(self, id, username, password, hashcode):
        UserMixin.__init__(self)
        self.id = id
        self.username = username
        self.password = password
        self.hashcode = hashcode

    def get_id(self):
        return unicode(self.id)

    # Password is in de database met prefix {SHA-1} opgeslagen.
    # Tevens is alles in uppercase in de database.
    def check_password(self, password):
        md5 = hashlib.md5()
        md5.update(password)
        if md5.hexdigest() == self.password:
            return True
        return False
