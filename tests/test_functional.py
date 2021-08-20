import allure
import pytest
from framework.api.json_converter import JsonConverter
from tests.config.urls import Urls
from tests.config.api_headers import RequestHeaders
from tests.routes.API import API
from tests.other_utils import MyUtils
from tests.config.json_fixture.create_post_json import CreatePostJSON
from tests.config.json_fixture.user_5_json import User5JSON

class TestFunctional(object):
      
    @pytest.mark.parametrize('headers, post_id_99, post_id_150, post_id_for_verif, \
                              post_userID_for_verif, user_5_json, user_5_query',
                            [(RequestHeaders.BASE_HEADERS, '/99', '/150',
                             99, 10, User5JSON.user_5_json(), '/5')])
    def test_rest_api(self, headers, post_id_99, post_id_150, 
                      post_id_for_verif, post_userID_for_verif,
                      user_5_json, user_5_query):
        with allure.step("Step №1 - Получаем посты и проверям, \
                          что они отсортировани по возрастанию id"):
          api_inst = API(headers)
          posts = api_inst.get_response_obj(Urls.POSTS_PATH)
          assert api_inst.check_list_sorted_ascending_order_id(posts), (
          'Посты сортируются не по возрастанию id'
          )
        with allure.step("Step №2 - Получаем пост номер 99, \
                           и проверяем что данные корректны"):
          post_99 = api_inst.get_response_obj(Urls.POSTS_PATH + post_id_99)
          assert api_inst.check_post_field(post_99, userId=post_userID_for_verif, 
                                           id=post_id_for_verif), (
                                           'Пост не соответсвует требования проверки')
        with allure.step("Step №3 - Получаем пост номер 150, \
                           и проверяем, что статус код равен 404"):
          assert api_inst.get(MyUtils.join_path(Urls.POSTS_PATH + post_id_150)).status_code == 404, (
                                          'Возникла ошибка в функции get_response_obj')
        with allure.step("Step №4 - Создаём пост, \
                          и проверяем, что он создался правильно с переданными данными"):
          text = MyUtils.generate_random_text(13)
          create_post_res = api_inst.post(MyUtils.join_path(Urls.POSTS_PATH), 
                                          CreatePostJSON.for_create_post(text))
          assert create_post_res.status_code == 201, 'Пост не был создан, произошла ошибка'
          post_101 = api_inst.get_response_obj(Urls.POSTS_PATH, query='/101')
          assert api_inst.check_post_field(post_101 ,body=text, title = text), 'Данные нового поста неккоректы'
        with allure.step("Step №5 - Получаем пользователей, \
                          и проверяем, что данные 5-ого пользователя\
                          отображаются правильно"):
          users = api_inst.get_response_obj(Urls.USERS_PATH)
          validat_data = JsonConverter.json_converter(user_5_json)
          assert api_inst.check_five_user_valid_data(users[4], 
                                                     validat_data),(
                                                     'Данные 5 пользователя не совпадают с ожидаемыми'
                                                     )
        with allure.step("Step №6 - Получаем пятого пользователя, \
                          и проверяем, что данные 5-ого пользователя\
                          отображаются правильно"):
          user_5 = api_inst.get_response_obj(Urls.USERS_PATH + user_5_query)
          assert api_inst.check_five_user_valid_data(user_5, 
                                                     validat_data),(
                                                     'Данные 5 пользователя не совпадают с ожидаемыми'
                                                     )