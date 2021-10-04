import json
import os
from types import SimpleNamespace

class JsonConverter:
    """Можно будет создать отделиный JSON класс, и поместить в него все поля объекта,
    нужно только передать имя Класса и указать в нем ожидаемые поля, далее объект будет расспрасен
    в классе и можно будет определять там другие методы или перегружать операторы, но в этом задании
    я не увидел смысла создавать отдельные классы.
    Функция была доработана теперь появилась возможность в авто-режиме представлять JSON ответ в виде 
    класса(не просто обьекта класса, а именно файла), не работает для ответов JSON в виде массива, для 
    этого придется создавать класс и определять все методы вручную. В параметрах нужно передать только 
    сам JSON ответ, имя класса который хотим создать и путь к папке в которох хотим создать
     """
    @staticmethod
    def json_converter(data, Class=None, dir_path=None, classname=None):
        try:
            data = data.json()
        except:
            pass
        if Class:
            if isinstance(data, list):
                obj_instanse = []
                for obj in data:
                    str_obj = json.dumps(obj)
                    obj_instanse.append(Class(JsonConverter.parse_json_into_obj(str_obj)))
                return obj_instanse
            else:
                str_obj = json.dumps(data)
                return Class(JsonConverter.parse_json_into_obj(str_obj))
        elif classname and dir_path:
            str_obj = json.dumps(data)
            return JsonConverter.create_class_file_from_json(data, classname=classname, 
                                                            dir_path=dir_path)
        else:
            if isinstance(data, list):
                obj_instanse = []
                for obj in data:
                    str_obj = json.dumps(obj)
                    obj_instanse.append(JsonConverter.parse_json_into_obj(str_obj))
                return obj_instanse
            else:
                str_obj = json.dumps(data)
                return JsonConverter.parse_json_into_obj(str_obj)

    @staticmethod
    def get_keys(_dict):
        return list(_dict.keys())

    @staticmethod
    def parse_json_into_obj(obj):
        return json.loads(obj, object_hook=lambda d: SimpleNamespace(**d))

    @staticmethod
    def create_class_file_from_json(json_obj, dir_path, classname):
        """Данная функция создаст файл(и в нем же класс)в папке которую нужно передать в параметре
        Файл будет автоматически заполнен по имени класса с базовой функцией __init_ и полями
        из JSON ответа"""
        work_dir = os.getcwd()
        json_keys, json_value = JsonConverter.dict_iterator_get_keys_and_val(json_obj)
        classname = str(classname).capitalize()
        with open(f"{work_dir}{dir_path}\{classname}.py", 'a+') as class_inst:
            class_inst.write(f'class {classname}:\n\n')
            class_inst.write(f'  def __init__(self):\n\n')
            for entry in range(len(json_keys)):
                class_inst.write(f"    self.{json_keys[entry]} = '{json_value[entry]}'\n")

    @staticmethod
    def dict_iterator_get_keys_and_val(dictionali, key_search=[]):
        """
        Данный метод обходит вложенные словари в глубину,
        разделяя ключи и значения в отдельные массивы для дальнейшего
        преобразования, также можно разделить только по тому ключю,
        по которому нужно, передав параметр key_search
        Вроде бы подхожит даже для самых страшных структур JSON:D
        """
        _key, _val = [], []
        def dict_iterator_v(dictionali, key_search):
            for key in dictionali:
               if key in key_search or len(key_search) == 0: 
                  if isinstance(dictionali[key], dict):
                     dict_iterator_v(dictionali[key], key_search)
                  else:
                      _val.append(dictionali[key])
            return _val
        """Получаем все ключи вложенного словаря"""
        def dict_iterator_k(dictionali, key_search):
            outer_keys = list(dictionali.keys())
            for key in outer_keys:
                if key in key_search or len(key_search) == 0:
                    if isinstance(dictionali[key], dict):
                        dict_iterator_k(dict(dictionali[key]), key_search)
                    else:
                        _key.append(key)
            return _key
        return  dict_iterator_k(dictionali, key_search), dict_iterator_v(dictionali, key_search)


