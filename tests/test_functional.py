"""Специализированные модули для тестирования и отчётов"""
from tests.pages.home_page import HomePage
import allure
import pytest

"""Модули из фреймворка"""
from framework.browser.browser import Browser

"""Тестовые данные"""
from tests.config.test_data.urls import Urls
from tests.config.test_data.t_data import Tdata
from tests.config.test_data.api_headers import RequestHeaders


"""Утилиты"""
from tests.routes.VKApi import VKApi
from tests.other_utils import MyUtils

"""Страницы"""
from tests.pages.vk_login_page import VKLoginPage
from tests.pages.home_page import HomePage
from tests.pages.my_page import MyPage

class TestFunctional(object):

      @pytest.mark.parametrize('headers, base_url, login_password, token, user_id,\
                                image_path',
                            [(RequestHeaders.BASE_HEADERS, Urls.VK_UI_URL,
                            (Tdata.EMAIL, Tdata.PASSWORD), Tdata.ACCESS_TOKEN,
                            Tdata.USER_ID, Urls.IMAGE_PATH)])
      def test_vk_api(self, headers, base_url, login_password, token, user_id,
                      image_path, create_browser):
            with allure.step("Step №1 - Перейти на сайт https://vk.com/"):
                 Browser.get_browser().set_url(base_url)
            with allure.step("Step №2 - Авторизоваться"):
                 login_page = VKLoginPage()
                 login_page.login(login_password)
            with allure.step("Step №3 -  Перейти на 'Мою страницу'"):
                 home_page = HomePage()
                 home_page.go_to_my_page()
            with allure.step("Step №4 -  С помощью запроса к API создать запись со случайно\
                              сгенерированным текстом на стене и\
                              получить id записи из ответ"):
                  api_inst = VKApi(headers, token)
                  message = MyUtils.generate_random_text(10)
                  api_inst.create_post_on_my_page(params=f'message={message}')
            with allure.step("Step №5 - Не обновляя страницу убедиться, что на стене появилась\
                              запись с нужным текстом от правильного пользователя"):
                  my_page = MyPage()
                  assert my_page.check_post_is_visiple_right(message, Tdata.AUTOR_NAME),(
                  'Только что созданный пост отображается неверно'
                   )
            with allure.step("Step №6 -  Отредактировать запись через запрос к API - изменить\
                              текст и добавить (загрузить) любую картинку"):
                  api_inst.edit_post_on_my_page(group_id=user_id, filepath=image_path)
                        


