from selenium.webdriver.common.by import By

"""Элементы"""
from framework.pages.base_page import BasePage


class MyPage(BasePage):
    unik_el = "//div[@class='profile_warning_label']"
   
    def __init__(self):
        super().__init__(search_condition=By.XPATH, 
                    locator=MyPage.unik_el,
                    page_name=self.__class__.__name__)
        self.post = None
        self.comment = None
        
        super().wait_for_page_opened()