import random
import string
from tests.config.urls import Urls

class MyUtils:
    

    @staticmethod
    def create_new_list_from_list(lis, key):
        try:
            new_list = []
            for i in lis:
                new_list.append(i[key])
            return new_list
        except TimeoutError as t:
            return t

    @staticmethod
    def generate_random_text(length):
            letters = list(string.ascii_letters)
            rand_str = ''
            for i in range(length):
                rand_str = rand_str + ''.join(random.choice(letters))
            return rand_str

    @staticmethod
    def dict_iterator_get_val(dictionali, key_search=[]):
        _val = []
        def dict_iterator(dictionali, key_search):
            for key in dictionali:
               if key in key_search or len(key_search) == 0: # Вернет толкько те занчения ключей которые мы зададим
                  if isinstance(dictionali[key], dict):
                     dict_iterator(dictionali[key], key_search)
                  else:
                      _val.append(dictionali[key])
            return _val
        return dict_iterator(dictionali, key_search)

    @staticmethod
    def checking_key_and_val_object(json_obj, verification_data, 
                            flag=False, ignore_key=''):
        keys =[]
        value = MyUtils.dict_iterator_get_val(json_obj)
        result = False
        k = 0
        try:
            keys = list(json_obj.keys())
        except:
            pass
        for i in range(len(value)):
                if isinstance(value[i], str):
                    if not flag:
                        if k > 0:
                            k-=1
                        if value[i]:
                            result = True
                        else:
                            result = False
                            break
                    else:
                        if value[i] == verification_data[k] or (ignore_key in keys[i]):
                            k+=1
                            result = True
                        else:
                            result = False
                            break
                if isinstance(value[i], int):
                    if value[i] == verification_data[k] or (ignore_key in keys[i]):
                        k+=1
                        result = True
                    else:
                        result = False
                        break
        return result

    @staticmethod
    def join_path(path, host = Urls.BASE_URL):
            host_path = host + path
            return host_path