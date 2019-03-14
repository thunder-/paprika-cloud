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

    # Password is stored as SHA512 string.
    def check_password(self, password):
        sha512 = hashlib.sha512()
        sha512.update(password)

        print self.password
        print sha512.hexdigest()
        if sha512.hexdigest() == self.password:
            return True
        return False
