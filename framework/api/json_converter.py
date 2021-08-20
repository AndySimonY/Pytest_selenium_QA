import json
from types import SimpleNamespace

class JsonConverter:
    """Можно будет создать отделиный JSON класс, и поместить в него все поля объекта,
    нужно только передать имя Класса и указать в нем ожидаемые поля, далее объект будет расспрасен
    в классе и можно будет определять там другие методы или перегружать операторы, но в этом задании
    я не увидел смысла создавать отдельные классы.
     """
    @staticmethod
    def json_converter(data, Class=None): 
        if Class:
            if isinstance(data, list):
                obj_instanse = []
                for obj in data:
                    str_obj = str(obj).replace("\'", "\"")
                    obj_instanse.append(Class(JsonConverter.parse_json_into_obj(str_obj)))
                return obj_instanse
            else:
                str_obj = str(data).replace("\'", "\"")
                return Class(JsonConverter.parse_json_into_obj(str_obj))
        else:
            if isinstance(data, list):
                obj_instanse = []
                for obj in data:
                    str_obj = str(obj).replace("\'", "\"")
                    obj_instanse.append(JsonConverter.parse_json_into_obj(str_obj))
                return obj_instanse
            else:
                str_obj = str(data).replace("\'", "\"")
                return JsonConverter.parse_json_into_obj(str_obj)
                      
    @staticmethod
    def parse_json_into_obj(obj):
        return json.loads(obj, object_hook=lambda d: SimpleNamespace(**d))