"""Специализированные модули для тестирования и отчётов"""
import allure
import pytest

"""Модули из фреймворка"""
from framework.browser.browser import Browser

"""Тестовые данные"""
from tests.config.test_data.urls import Urls
from tests.config.test_data.t_data import Tdata
from tests.config.test_data.api_headers import RequestHeaders
from tests.config.test_data.vk_locators.menu_loc import LeftMainMenu

"""Утилиты"""
from tests.routes.VKApi import VKApi
from tests.MyUtils.other_utils import MyUtils

"""Страницы"""
from tests.pages.vk_login_page import VKLoginPage
from tests.pages.my_page import MyPage
from tests.pages.feed_page import FeedPage

"""Сторонние сущности"""
from tests.pages.wall.wall_posts_entity import PostsForm
from tests.pages.wall.wall_comments_entity import CommentForm


class TestFunctional(object):

      @pytest.mark.parametrize('headers, base_url, login_password, token,\
                                image_path, my_page_loc',
                            [(RequestHeaders.BASE_HEADERS, Urls.VK_UI_URL,
                            (Tdata.EMAIL, Tdata.PASSWORD), Tdata.ACCESS_TOKEN,
                             Urls.LEOPARD_IMAGE_PATH, LeftMainMenu.my_page)])
      def test_vk_api(self, headers, base_url, login_password, 
                      token, image_path,my_page_loc, create_browser):
                      
          with allure.step("Step №1 - Перейти на сайт https://vk.com/"):
                 Browser.get_browser().set_url(base_url)

          with allure.step("Step №2 - Авторизоваться"):
                 login_page = VKLoginPage()
                 login_page.login(login_password)
                 
          with allure.step("Step №3 -  Перейти на 'Мою страницу'"):
                 FeedPage(locator=my_page_loc).main_menu_left.navigate()

          with allure.step("Step №4 - Получить изображение"):
                 img = Img()
                 img_el = img.get_image()
                 assert not img_el, "sdsdsdsd"

          with allure.step("Step №4.1 -  С помощью запроса к API получить id \
                              текущего пользователя"):
                  api_inst = VKApi(headers, token)
                  user_id = api_inst.get_current_user()
                 
          with allure.step("Step №4.2 -  С помощью запроса к API создать запись со случайно\
                              сгенерированным текстом на стене и\
                              получить id записи из ответ"):
                  message_step_4 = MyUtils.generate_random_text(10)
                  post_id = api_inst.create_post_on_my_page(message=message_step_4)

          with allure.step("Step №5 - Не обновляя страницу убедиться, что на стене появилась\
                              запись с нужным текстом от правильного пользователя"):
                  my_page = MyPage()
                  wall_post = my_page.post = PostsForm(user_id=user_id, post_id=post_id)
                  assert wall_post.check_post_is_visiple_right(message_step_4, Tdata.AUTOR_NAME),(
                  'Только что созданный пост отображается неверно'
                   )

          with allure.step("Step №6 -  Отредактировать запись через запрос к API - изменить\
                              текст и добавить (загрузить) любую картинку"):
                  message_step_6 = MyUtils.generate_random_text(10)
                  photo_id = api_inst.edit_post_on_my_page(
                             post_id=post_id, message=message_step_6,
                             owner_id=user_id, filepath=image_path
                                                )
          with allure.step("Step №7 -   Не обновляя страницу убедиться, что изменился\
                               текст сообщения и добавилась загруженная\
                               картинка(убедиться, что картинки одинаковые)"):
                  wall_post_with_photo = my_page.post = PostsForm(user_id=user_id, 
                                                                  post_id=post_id, photo_id=photo_id)
                  assert wall_post_with_photo.check_post_changes_and_added_img(
                                 message_step_6),(
                                   "Во время изменения поста(текст, добавлен фото), произошла ошибка")

          with allure.step("Step №8 - Используя запрос к API добавить комментарий к\
                              записи со случайным текстом"):
               message_step_8 = MyUtils.generate_random_text(10)
               comment_id = api_inst.create_comment(owner_id=user_id, 
                                       post_id=post_id,
                                       message=message_step_8)

          with allure.step("Step №9 - Не обновляя страницу убедиться, что на стене появилась\
                              запись с нужным текстом от правильного пользователя"):

               wall_comment = MyPage().comment = CommentForm(user_id=user_id, 
                                                             post_id=post_id,
                                                             comment_id=comment_id)
               assert wall_comment.check_comment_visible_right(message_step_8, Tdata.AUTOR_NAME), (
                    'Коммент отображается неверно'
               )

          with allure.step("Step №10 - Через UI оставить лайк к записи"):
               like = wall_post.like_btn
               like.add_like_post()

          with allure.step("Step №11 - Через запрос к API убедиться, что у записи\
                            появился лайк от правильного пользователя"):
               assert api_inst.check_add_like_this_post(owner_id=user_id, post_id=post_id), (
                      'Нужного пользователя нет в спискепролайкавших')

          with allure.step("Step №12 - Через запрос к API удалить созданную запись"):
               api_inst.delete_entry(owner_id=user_id, post_id=post_id)

          with allure.step("Step №13 - Не обновляя страницу убедиться, что запись удалена"):
               assert wall_post.check_post_is_deleted(), "Ошибка при удалени, новосозданный пост не был удалён"