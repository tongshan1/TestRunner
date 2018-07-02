from .util import set_variable
from requests import Response


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

        self.text = api_response.text
        try:
            self.data = api_response.json()
        except ValueError:
            self.data = self.text
        super().__init__()

    def __repr__(self):
        return str(self.data)

    def get_value_by_key(self, key):

        if not key:
            return
        tmp = "self.data."+key
        return eval(tmp)

    def validate(self, verification):
        """
        result : 1 pass
                 2 error
                 3 fail
        :param verification:
        :return:
        """
        result = 1

        for key, value in verification.items():

            real_value = self.get_value_by_key(key)

            # 如果需要保存
            if value[1]:
                set_variable(key, self.get_value_by_key(key))

            v_type = value[2]
            v_value = value[0]
            # 验证值
            if v_type == "None":
                continue

            # 转换类型
            try:
                if v_type == "str":
                    v_value = str(v_value)
                if v_type == "int":
                    v_value = int(v_value)
                if v_type == "float":
                    v_value = float(v_value)
                if v_type == "list":
                    v_value = list(v_value)
                if v_type == "dict":
                    v_value = dict(v_value)
                if real_value != v_value:
                    result = 3
            except ValueError:
                result = 3

        return result
