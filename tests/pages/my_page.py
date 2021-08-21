from selenium.webdriver.common.by import By

"""Элементы"""
from framework.pages.base_page import BasePage
from framework.elements.text_box import TextBox
from framework.elements.label import Label
from framework.elements.button import Button
from framework.elements.link import Link


class MyPage(BasePage):

    header = ".//header[@id = 'page_header']"
    wall_post_text = Label(search_condition=By.XPATH,
                           locator=".//div[contains(@class, 'wall_post_text')]", 
                           name='My new Post text')
    wall_post_autor = Link(search_condition=By.XPATH,
                           locator=".//a[@class='author']", 
                           name='My new Post autor')

    def __init__(self):
        super().__init__(search_condition=By.XPATH, 
                    locator=MyPage.header,
                    page_name=self.__class__.__name__)
        super().wait_for_page_opened()


    def check_post_is_visiple_right(self, text, autor_name):
        if self.wall_post_text.get_text() == text and\
           self.wall_post_autor.get_text() == autor_name:
           return True
        else: return False
