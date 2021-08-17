from framework.pages.base_page import BasePage
from selenium.webdriver.common.by import By
from framework.elements.text_box import TextBox
from framework.elements.label import Label
from framework.elements.button import Button

class WelcomePage(BasePage):
     
    logo = ".//div[@class='logo__icon']"
    def __init__(self):
        super().__init__(search_condition=By.XPATH, 
                         locator=WelcomePage.logo,
                         page_name=self.__class__.__name__)
        super().wait_for_page_opened()