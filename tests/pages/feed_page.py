from selenium.webdriver.common.by import By

"""Элементы"""
from framework.pages.base_page import BasePage

"Отдельные сущности страницы"
from tests.pages.menu.main_menu_entity import MainMenu

class FeedPage(BasePage):

    header = "//header[@id = 'page_header']"
   
    def __init__(self, locator=''):
        super().__init__(search_condition=By.XPATH, 
                    locator=FeedPage.header,
                    page_name=self.__class__.__name__)
        if locator:
            self.main_menu_left = MainMenu(locator=locator) 
        super().wait_for_page_opened()
    