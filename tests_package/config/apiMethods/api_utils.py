from framework.api.base_api import BaseApi
from framework.jsonUtils.json_converter import JsonConverter
from framework.xmlUtils.xml_converter import XMLConverter

from config.api_config.status_code import StatusCode
from config.test_conf.some_conditions import Cond

class ApiUtils(BaseApi):

    def __init__(self, headers):
        super().__init__(headers)
      
    def get_books(self, url):
        response = self.get(url=url)
        assert response.status_code == StatusCode.STATUS, "Запрос провалился либо был отправлен неверно"
        assert XMLConverter.is_xml(response.text), "Данные вернулись в отличном от XML формате"
        books = JsonConverter.json_converter(
                XMLConverter.from_xml_to_dict(response.text, 
                                              condit=Cond.some_conditions) # Конвертируем XML в 
                                              # строковое представление словаря
                ) # Конвертируем в JSON и попутно создаём модель JSON ответа в виде объекта класса
        return books