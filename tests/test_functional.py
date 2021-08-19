
import allure
import pytest
from tests.config.urls import Urls
from tests.config.test_data import TestData
from tests.config.api_headers import RequestHeaders
from tests.routes.API import API
from tests.other_utils import MyUtils
from tests.config.json_fixture import JSONFixture



class TestFunctional(object):
      
    @pytest.mark.parametrize('url_path, headers', 
                            [(Urls.POSTS_PATH, 
                              RequestHeaders.BASE_HEADERS)])
    def test_posts_response(self, url_path, headers,wait_for_next_request):
        with allure.step("GET posts"):
          api_inst = API(headers)
          posts_res = api_inst.get(MyUtils.join_path(url_path))
          assert posts_res.status_code == 200, 'Запрос провалился'
        with allure.step("Check response is json"):
          json_obj = api_inst.check_is_json(posts_res)
          assert json_obj, "Кажется это не JSON формат"
        with allure.step("The list is sorted in ascending order"):
          assert api_inst.check_list_sorted_ascending_order(json_obj), 'ID сортируются не по возрастанию'

    @pytest.mark.parametrize('url_path, headers, validation_data',  
                            [(Urls.POST_99, 
                              RequestHeaders.BASE_HEADERS, [10, 99])])
    def test_post_number_99(self, url_path, headers,
                      validation_data, wait_for_next_request):
        with allure.step("GET post number 99"):
          api_inst = API(headers)
          posts_res = api_inst.get(MyUtils.join_path(url_path))
          assert posts_res.status_code == 200, 'Запрос провалился'
        with allure.step("Check response is json"):
          json_obj = api_inst.check_is_json(posts_res)
          assert json_obj, "Кажется это не JSON формат"
        with allure.step("Check post 99 is displayed correctly"):
          assert api_inst.post_99_is_displayed_correctly(json_obj, validation_data), (
                                                        'Значения не совпадают с ожидаемыми')

    @pytest.mark.parametrize('url_path, headers',  
                            [(Urls.POST_150, 
                              RequestHeaders.BASE_HEADERS)])
    def test_404(self, url_path, headers, wait_for_next_request):
        with allure.step("GET post number 150"):
          api_inst = API(headers)
          posts_res = api_inst.get(MyUtils.join_path(url_path))
          assert posts_res.status_code == 404, 'Запрос каким то образом не провалился'

    @pytest.mark.parametrize('url_path, headers, my_post_id',
                            [(Urls.POSTS_PATH, 
                              RequestHeaders.BASE_HEADERS, '/101')])
    def test_create_post(self, url_path, headers, my_post_id):
        with allure.step("POST request - create post"):
          api_inst = API(headers)
          text = api_inst.get_random_text(13)
          posts_res = api_inst.post(MyUtils.join_path(url_path), 
                                    JSONFixture.for_create_post(text))
          assert posts_res.status_code == 201, 'Пост должен быть создан'
        with allure.step("Get my new creating post"):
          posts_res = api_inst.get(MyUtils.join_path(url_path) + my_post_id)
          assert posts_res.status_code == 200, 'Пост не получен'
        with allure.step("Check response is json"):
           json_obj = api_inst.check_is_json(posts_res)
           assert json_obj, "Кажется это не JSON формат"
        with allure.step("Check my new post is displayed correctly"):
          if posts_res.status_code == 200:
              assert api_inst.check_new_my_post_is_displayed_correctly(json_obj, 
                                                                      [text, text, 1], 
                                                                      'id')

    @pytest.mark.parametrize('url_path, headers, user_num, verif_value',
                            [(Urls.USERS_PATH, 
                              RequestHeaders.BASE_HEADERS, 5, 
                              TestData.VALUES_FOR_5_USER)])
    def test_get_users(self, url_path, headers, 
                       user_num, verif_value, wait_for_next_request):
      with allure.step("Get users"):
        api_inst = API(headers)
        posts_res = api_inst.get(MyUtils.join_path(url_path))
        assert posts_res.status_code == 200, 'Пользователи не получены'
      with allure.step("Check response is json"):
          json_obj = api_inst.check_is_json(posts_res)
          assert json_obj, "Кажется это не JSON формат"
      with allure.step("Check 5 user is displayed correctly"):
          assert api_inst.check_5_user_is_displayed_correctly(json_obj[user_num - 1], verif_value), (
                'Данныйе 5-ого пользователя не совпадают')

    @pytest.mark.parametrize('url_path, headers, verif_value',
                            [(Urls.USER_5, 
                              RequestHeaders.BASE_HEADERS,
                              TestData.VALUES_FOR_5_USER)])
    def test_get_users_5(self, url_path, headers, verif_value,
                       wait_for_next_request):
      with allure.step("Get users five"):
        api_inst = API(headers)
        posts_res = api_inst.get(MyUtils.join_path(url_path))
        assert posts_res.status_code == 200, 'Пользователи не получены'
      with allure.step("Check response is json"):
          json_obj = api_inst.check_is_json(posts_res)
          assert json_obj, "Кажется это не JSON формат"
      with allure.step("Check 5 user is displayed correctly"):
          assert api_inst.check_again_5_user_is_displayed_correctly(json_obj, verif_value), (
            'Данный пользователя 5 не соответсвуют предидущим полученным данным'
          )