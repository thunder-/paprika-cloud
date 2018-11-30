class DictExt:
    def __init__(self):
        pass

    @staticmethod
    def strip_none(d):
        if d:
            result = {}
            keys = d.keys()
            for key in keys:
                result[key] = d[key]
                if not d[key]:
                    result[key] = ''
            return result
        return d
