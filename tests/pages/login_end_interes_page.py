from logging import error
import time
import pyautogui
from framework.pages.base_page import BasePage
from selenium.webdriver.common.by import By
from framework.elements.text_box import TextBox
from framework.elements.link import Link
from framework.elements.label import Label
from framework.elements.button import Button
from selenium.webdriver.common.keys import Keys
from framework.browser.browser import Browser
from tests.other_utils import generate_random_number
from tests.config.urls import Urls



class LoginAndInteresPage(BasePage):
    search_condition = By.XPATH

    div_logo = ".//div[@class='logo__icon']"
    click_here_link = Button(search_condition=search_condition, 
                             locator=".//a[@class='start__link']",
                             name="Click HERE button")
    div_login_form = Label(search_condition=search_condition, 
                           locator=".//div[@class='login-form__container']", 
                           name="Login Form Box")
    inp_password = TextBox(search_condition=search_condition,
                           locator=".//input[@placeholder='Choose Password']", 
                           name='Choose Password')
    inp_email = TextBox(search_condition=search_condition,
                        locator=".//input[@placeholder='Your email']", 
                        name='Your email')
    inp_domain = TextBox(search_condition=search_condition,
                        locator=".//input[@placeholder='Domain']", 
                        name='Domain')
    div_dropdown = Button(search_condition=search_condition,
                          locator=".//div[@class='dropdown__opener']", 
                          name='Dropdown Opener')
    div_dropdown_item = Label(search_condition=search_condition,
                        locator=".//div[@class='dropdown__list']/div[text() = '.org']", 
                        name='Dropdown .org')
    sp_checkbox_politic = Button(search_condition=search_condition,
                         locator="//span[contains(@class,'icon-check')]",
                         name='CheckBox')
    btn_next = Button(search_condition=search_condition,
                      locator=".//a[contains(@class, 'button--secondary') or text() = 'Next']",
                      name='CheckBox')
    inf_field = Label(search_condition=search_condition,
                      locator=".//div[@class='avatar-and-interests']",
                      name='Information Field')
    sp_checkbox_interes = Button(search_condition=search_condition,
                                  locator=".//div[@class='avatar-and-interests__interests-list__item']//span[@class='checkbox__box']",
                                  name='Checkbox Interes')
    a_upload_img = Link(search_condition=search_condition,
                           locator=".//a[@class='avatar-and-interests__upload-button']",
                           name='Upload Image'
                                )
    btn_next_of_user_inf_side = Button(search_condition=search_condition,
                                       locator=".//button[contains(@class,'button--stroked')]",
                                       name='Button Next')
    div_personal_details = Label(search_condition=search_condition,
                                 locator=".//div[@class='personal-details__form']",
                                 name='Personal inf. details')
    help_window = Label(search_condition=search_condition,
                        locator=".//div[contains(@class,'help-form')]",
                        name='Help window')
    div_cookie = Label(search_condition=search_condition,
                       locator=".//div[@class='cookies']",
                       name='Cookie form')
    btn_close_help_window = Label(search_condition=search_condition,
                                  locator=".//button[contains(@class, 'help-form__send')]",
                                  name='Button for close help window')
    btn_accept_cookie = Button(search_condition=search_condition,
                               locator=".//button[text() = 'Not really, no'] ",
                               name='Button for accept cookie')
    div_timer = Label(search_condition=search_condition,
                      locator=".//div[contains(@class,'timer')]",
                      name='Button for accept cookie')

    def __init__(self):
        super().__init__(search_condition=LoginAndInteresPage.search_condition, 
                         locator=LoginAndInteresPage.div_logo,
                         page_name=self.__class__.__name__)
        super().wait_for_page_opened()


    def is_autorization_form_displayed(self):
        self.click_here_link.click()
        return self.div_login_form.is_disabled
    
    def login(self, password, email, domain):
        self.inp_password.clear_field()
        self.inp_password.send_keys(password)

        self.inp_email.clear_field()
        self.inp_email.send_keys(email)

        self.inp_domain.clear_field()
        self.inp_domain.send_keys(domain)

        self.div_dropdown.click()
        self.div_dropdown_item.click()

        self.sp_checkbox_politic.click()
        self.btn_next.click()
        return self.inf_field.is_disabled

    def select_int_and_upload_img(self):
        lis = self.sp_checkbox_interes.get_elements()
        lis[20].click()
        number_of_interes = generate_random_number()
        for el in range(len(number_of_interes)):
            lis[number_of_interes[el]].click()
        self.a_upload_img.click()
        time.sleep(2) #Небольшое ожидание открытия диалогового окна ОС
        pyautogui.write(Urls.PATH_FOR_UPLOAD_IMAGE)
        pyautogui.press('enter')
        time.sleep(1) # Ожидание закрытия окна, далее продолжаем тетирование
        self.btn_next_of_user_inf_side.click()
        return self.div_personal_details.is_displayed

    def help_window_must_be_hidden(self):
        self.click_here_link.click()
        self.btn_close_help_window.click()
        if self.help_window.get_attribute_class() == 'help-form is-hidden':
             return True
        else:
            return False
    
    def accept_cookie(self):
        self.click_here_link.click()
        self.btn_accept_cookie.wait_for_is_visible()
        self.btn_accept_cookie.click()
        self.div_cookie.wait_for_invisibility()
        return self.div_cookie.is_disabled

    def check_timer_starts_from_zero(self):
        self.click_here_link.click()
        if self.div_timer.get_text() == '00:00:00':
            return True
        else: 
            return False
 