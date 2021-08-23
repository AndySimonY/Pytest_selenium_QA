from selenium.webdriver.common.by import By

"""Элементы"""
from framework.pages.base_page import BasePage
from framework.elements.button import Button

class LikeForm(BasePage):

    post_field = ".//div[@id='post_field']"

    add_like_btn = Button(search_condition=By.XPATH,
                           locator="//div[@class='like_btns']/div", 
                           name='Like btn')



    def __init__(self):
        super().__init__(search_condition=By.XPATH, 
                    locator=LikeForm.post_field,
                    page_name=self.__class__.__name__)
        super().wait_for_page_opened()


    def add_like(self):
        self.add_like_btn.click()