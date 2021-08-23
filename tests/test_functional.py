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
from tests.pages.wall.wall_posts_form import WallPosts
from tests.pages.wall.wall_comments_form import WallComments
from tests.pages.wall.wall_like_form import LikeForm

class TestFunctional(object):

      @pytest.mark.parametrize('headers, base_url, login_password, token, user_id,\
                                image_path',
                            [(RequestHeaders.BASE_HEADERS, Urls.VK_UI_URL,
                            (Tdata.EMAIL, Tdata.PASSWORD), Tdata.ACCESS_TOKEN,
                            Tdata.USER_ID, Urls.LEOPARD_IMAGE_PATH)])
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
                  message_step_4 = MyUtils.generate_random_text(10)
                  post_id = api_inst.create_post_on_my_page(params=f'message={message_step_4}')
          with allure.step("Step №5 - Не обновляя страницу убедиться, что на стене появилась\
                              запись с нужным текстом от правильного пользователя"):
                  wall_post = WallPosts()
                  assert wall_post.check_post_is_visiple_right(message_step_4, Tdata.AUTOR_NAME),(
                  'Только что созданный пост отображается неверно'
                   )
          with allure.step("Step №6 -  Отредактировать запись через запрос к API - изменить\
                              текст и добавить (загрузить) любую картинку"):
                  message_step_6 = MyUtils.generate_random_text(10)
                  photo_id = api_inst.edit_post_on_my_page(params=[
                  f'owner_id={user_id}', f'post_id={post_id}',
                  f'message={message_step_6}'],
                    owner_id=user_id, filepath=image_path
                                                )
          with allure.step("Step №7 -   Не обновляя страницу убедиться, что изменился\
                               текст сообщения и добавилась загруженная\
                               картинка(убедиться, что картинки одинаковые)"):
                  assert wall_post.check_post_changes_and_added_img(
                                 message_step_6, photo_id),(
                                   "Во время изменения поста(текст, добавлен фото), произошла ошибка")
          with allure.step("Step №8 - Используя запрос к API добавить комментарий к\
                              записи со случайным текстом"):
               message_step_8 = MyUtils.generate_random_text(10)
               api_inst.create_comment(params=[f'owner_id={user_id}',
               f'post_id={post_id}', f'message={message_step_8}'])
          with allure.step("Step №9 - Не обновляя страницу убедиться, что на стене появилась\
                              запись с нужным текстом от правильного пользователя"):
               wall_comment = WallComments()
               assert wall_comment.check_comment_visiple_right(message_step_8, Tdata.AUTOR_NAME), (
                    'Коммент отображается неверно'
               )
          with allure.step("Step №10 - Через UI оставить лайк к записи"):
               like = LikeForm()
               like.add_like()
          with allure.step("Step №11 - Через запрос к API убедиться, что у записи\
                            появился лайк от правильного пользователя"):
               assert api_inst.check_add_like_this_post(user_id=user_id,params=['type=post', 
               f'owner_id={user_id}', f'item_id={post_id}','filter=likes']), 'Нужного пользователя нет в списке\
                                                               пролайкавших'
          with allure.step("Step №12 - Через запрос к API удалить созданную запись"):
               api_inst.delete_entry(params=[f'owner_id={user_id}', f'post_id={post_id}'])
          with allure.step("Step №13 - Не обновляя страницу убедиться, что запись удалена"):
               assert wall_post.check_post_is_deleted(), "Ошибка при удалени, новосозданный пост не был удалён"