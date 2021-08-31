from framework.pages.base_page import BasePage
from selenium.webdriver.common.by import By
from framework.elements.text_box import TextBox
from framework.elements.label import Label
from framework.elements.button import Button

class LoginPage(BasePage):
     
    
    logo = ".//div[@class='logo__icon']"
    click_here_link = Button(search_condition=By.XPATH, 
                             locator=".//a[@class='start__link']",
                             name="Click HERE button")
    login_form = Label(search_condition=By.XPATH, 
                           locator=".//div[@class='login-form__container']", 
                           name="Login Form Box")
    help_window = Label(search_condition=By.XPATH,
                        locator=".//div[contains(@class,'help-form')]",
                        name='Help window')
    cookie = Label(search_condition=By.XPATH,
                       locator=".//div[@class='cookies']",
                       name='Cookie form')
    button_close_help_window = Label(search_condition=By.XPATH,
                                  locator=".//button[contains(@class, 'help-form__send')]",
                                  name='Button for close help window')
    button_accept_cookie = Button(search_condition=By.XPATH,
                               locator=".//button[text() = 'Not really, no'] ",
                               name='Button for accept cookie')


    def __init__(self):
        super().__init__(search_condition=By.XPATH, 
                         locator=LoginPage.logo,
                         page_name=self.__class__.__name__)
        super().wait_for_page_opened()

    def is_autorization_form_displayed(self):
        self.click_here_link.click()
        return self.login_form.is_displayed

    def click_close_help_window_buttom(self):
        self.button_close_help_window.click()    

    def get_class_style_of_help_window(self):
        if self.help_window.get_attribute_class() == 'help-form is-hidden':
            return True
        else:
            return False
        
    def click_button_accept_cookie(self):
        self.button_accept_cookie.wait_for_is_visible()
        self.button_accept_cookie.click()
    
    def is_invisibility_cookie_form(self):
        self.cookie.wait_for_invisibility()
        return self.cookie.is_disabled
    