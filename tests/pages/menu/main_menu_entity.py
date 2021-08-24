
from framework.elements.label import Label

from selenium.webdriver.common.by import By

class MainMenu:

     def __init__(self, locator):
          self.my_page = Label(search_condition=By.XPATH,
                    locator=locator, 
                    name='My Page') 
     
     def navigate(self):
          self.my_page.click()

         

        