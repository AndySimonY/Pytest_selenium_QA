from logging import fatal
from framework.api.base_api import BaseApi
from framework.utils.logger import Logger
from tests.other_utils import MyUtils

class API(BaseApi):

    def __init__(self, headers):
        super().__init__(headers)

    def check_is_json(self, json_obj):
        return self.get_json(json_obj)

    @staticmethod
    def check_list_sorted_ascending_order(json_obj):
        Logger.info("Проверяем что список сортируется корректно (по id)")
        id_list = MyUtils.create_new_list_from_list(json_obj, 'id')
        if id_list == sorted(id_list):
            return True
        else:
            return False

    @staticmethod
    def post_99_is_displayed_correctly(json_obj, 
                                       verification_data):
        """ В параметры передовать список только численных значений для проверки значений ключей в обьекте
            в том порядка в котором они указаны в объекте, если в объекте между ключами с
            численными значениям есть еще и строки  - это не повлияет. Но если предать доп параметрами 
            flag и ignore_keys, то сравнит все ключи обьекта со значениями переданными в списке в порядке ключей,
            будут игнорироваться и проверяться только на присутсвие ключи которые указаты в списке ignore_keys
            """
        return MyUtils.checking_key_and_val_object(json_obj, verification_data)

    @staticmethod
    def get_random_text(lenght=5):
        return MyUtils.generate_random_text(lenght)

    @staticmethod
    def check_new_my_post_is_displayed_correctly(json_obj, verification_data, ignore_key):
        return MyUtils.checking_key_and_val_object(
                                  json_obj,
                                  verification_data, 
                                  flag=True, 
                                  ignore_key=ignore_key)
   
    @staticmethod
    def check_5_user_is_displayed_correctly(json_obj, verification_data):
        return MyUtils.checking_key_and_val_object(
                                  json_obj,
                                  verification_data, 
                                  flag=True)

    def check_again_5_user_is_displayed_correctly(self, json_obj, verification_data):
        return MyUtils.dict_iterator_get_val(json_obj) == verification_data