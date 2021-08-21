from selenium.webdriver.common.by import By

"""Элементы"""
from framework.pages.base_page import BasePage
from framework.elements.text_box import TextBox
from framework.elements.label import Label
from framework.elements.button import Button



class VKLoginPage(BasePage):

     header = ".//header[@id = 'page_header']"
     email_index = TextBox(search_condition=By.XPATH,
                        locator=".//input[@id='index_email']", 
                        name='Email')
     password_index = TextBox(search_condition=By.XPATH,
                        locator=".//input[@id='index_pass']", 
                        name='Password')
     login_btn = Button(search_condition=By.XPATH,
                        locator=".//button[@id='index_login_button']", 
                        name='Sign in')

     def __init__(self):
          super().__init__(search_condition=By.XPATH, 
                         locator=VKLoginPage.header,
                         page_name=self.__class__.__name__)
          super().wait_for_page_opened()

     def login(self, login_data):

        email, password = login_data

        self.email_index.clear_field()
        self.email_index.send_keys(email)

        self.password_index.clear_field()
        self.password_index.send_keys(password)

        self.login_btn.click()




