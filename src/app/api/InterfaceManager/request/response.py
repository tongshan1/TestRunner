from .util import set_variable

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

        try:
            self.data = api_response.json()
        except ValueError:
            self.data = api_response.text
        super().__init__()

    def __repr__(self):
        return str(self.data)

    def get_value_by_key(self, key):
        return eval("self.data."+key)

    def validate(self, verification):
        result = True

        for key, value in verification.items():

            real_value = self.get_value_by_key(key)

            # 如果需要保存
            if value[1]:

                set_variable(key, self.get_value_by_key(key))

            if value[0] is None:
                pass
            if real_value != value[0]:
                result =  False

        return result
