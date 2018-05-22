
class DictObj(dict):
    def __init__(self):
        dict.__init__(self)

    def __getitem__(self, key):
        return self.__dict__[key]

    def __repr__(self):
        return str(self.__dict__)

    def __setattr__(self, key, value):
        x = {}
        y = DictObj()

        if hasattr(value, "__dict__"):
            x = vars(value)
        elif isinstance(value,dict):
            x = value
        else:
            x = value

        if isinstance(x, dict):
            for k in x.keys():
                setattr(y, k, x[k])
        else:
            y = x

        self.__dict__[key] = y

    def __setitem__(self, key, value):
        if hasattr(value, "__dict__"):
            v = DictObj(value)
        else:
            v = value

        setattr(self, key, v)


class ApiResponse(DictObj):

    def __init__(self, api_response):
        self.api_response = api_response
        self.dict = self.data
        super().__init__()

    @property
    def data(self):
        try:
            data = self.api_response.json()
        except ValueError:
            data = self.api_response.text
        return data

    def get_value_by_key(self, key):
        return eval("self.dict."+key)

    def validate(self, key, value):

        real_value = self.get_value_by_key(key)

        return real_value == value