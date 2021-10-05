"""Test dependencies"""
import pytest

"""Framework dependencies"""
from framework.browser.browser import Browser

"""Test data"""
from tests_package.config.t_data.web_urls import WebUrls

"""Test methods"""
from tests_package.step_tests import StepTests

"""Logs"""
from framework.utils.logger import Logger

"""Pages"""
from tests_package.pages.TreeDPanner_page import TreeDPannerPage

class TestFunctional(object):

     def test_treeD_Panner(self, create_browser):

          Logger.info("Шаг 1: Переходим на сайт https://roomstyler.com/3dplanner")
          Browser.get_browser().set_url(WebUrls.BASE_URL)
          treeDPannerPage = TreeDPannerPage()
          assert treeDPannerPage.render_window.is_displayed(), "Нужная страница открыта неккоректно"

          Logger.info("Шаг 2: Закрываем диалоговое окно: Welcome to roomstyler 3D home planner")
          treeDPannerPage.close_dialog_window()
          assert not treeDPannerPage.dialog_window_is_visible(), "Диалоговое окно не закрылось"

          Logger.info("Шаг 3: Открываем меню 'Furnish your room'")
          sidebar_menu = treeDPannerPage.sidebar_buttons_item # Панель инструментов слева
          sidebar_menu.navigate(locator=sidebar_menu.furnish_your_room)
          assert sidebar_menu.menu_is_displayed(sidebar_menu.furnish_your_room), (
          "'Furnish your room' не раскрылся")

          Logger.info("Шаг 4: Переходим в “Dining room”")
          sidebar_menu.navigate(locator=sidebar_menu.sub_menu_during_room)
          during_room_menu_items = sidebar_menu.get_menu_items(sidebar_menu\
                                               .sub_menu_during_room_elements,
                                               is_list=True)
          assert during_room_menu_items, ("Список элементов не появился")

          Logger.info("Шаг 5: Выбираем любой Drag and Drop item и переносим в рабочее пространство")
          

          

