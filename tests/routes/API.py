from framework.api.base_api import BaseApi
from framework.utils.logger import Logger
from framework.api.json_converter import JsonConverter
from tests.other_utils import MyUtils

class API(BaseApi):

    def __init__(self, headers):
        super().__init__(headers)


    def get_response_obj(self, url, query = '', status = 200, Class=None):
        response = self.get(MyUtils.join_path(url) + query)
        assert response.status_code == 200, 'Запрос провалился'
        json_obj = self.get_json(response)
        assert json_obj, "Кажется это не JSON формат"
        return JsonConverter.json_converter(json_obj, Class=Class)
    
    @staticmethod
    def check_list_sorted_ascending_order_id(obj):
        Logger.info("Проверяем что список сортируется по возрастанию id)")
        id_list = MyUtils.get_id_list(obj)
        if id_list == sorted(id_list):
            return True
        else:
            return False

    @staticmethod
    def check_five_user_valid_data(received_data, expected_data):
        if expected_data == received_data:
            return True
        else:
            return False

    @staticmethod
    def check_post_field(obj, id=None, userId=None, body='', title=''):
        result = False
        if body and not title:
            if obj.id and obj.title and obj.body == body and obj.userId == userId:
                result = True
        elif title and not body:
            if obj.id and obj.userId == userId and obj.title == title and obj.body:
                result = True
        elif title and body: 
             if obj.id and obj.userId == userId and obj.title == title and obj.body == body:
                result = True
        else:
            if obj.id == id and obj.userId == userId and obj.title and obj.body:
                result = True
        return result
    
    @staticmethod
    def get_json(json_obj):
        Logger.info("Получаем и проверяем что это JSON")
        try:
            j = json_obj.json()
        except ValueError as e:
            Logger.info("Неудалось получить JSON из запроса")
            return False
        return j