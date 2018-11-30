import os


class Finder(object):
    @staticmethod
    def open(filename, default=None):
        if os.path.exists(filename):
            return open(filename)
        if default:
            return open(os.path.join(default, filename))
