class EasyDict:
    def __init__(self, data: dict):
        self._dict = data

    def update(self, data):
        self._dict.update(data)

    def __iter__(self):
        return self._dict.__iter__()

    def __setattr__(self, attrname, value):
        if attrname == '_dict':
            return super(EasyDict, self).__setattr__(attrname, value)

        self._dict[attrname] = value

    def __getattr__(self, attrname):
        if attrname in self._dict:
            attvalue = self._dict[attrname]
            if isinstance(attvalue, dict):
                return EasyDict(attvalue)
            else:
                return attvalue

        return None

    def __getitem__(self, key):
        return self.__getattr__(key)

    def __setitem__(self, key, value):
        return self.__setattr__(key, value)

    def __repr__(self):
        return str(self._dict)