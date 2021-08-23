from selenium.webdriver.common.by import By

"""Элементы"""
from framework.pages.base_page import BasePage
from framework.elements.label import Label

class HomePage(BasePage):

    header = ".//header[@id = 'page_header']"
    my_page = Label(search_condition=By.XPATH,
                    locator=".//span[@class='left_label inl_bl' or text()='Моя страница']", 
                    name='My Page')

    def __init__(self):
        super().__init__(search_condition=By.XPATH, 
                    locator=HomePage.header,
                    page_name=self.__class__.__name__)
        super().wait_for_page_opened()
    
    def go_to_my_page(self):
        self.my_page.click()