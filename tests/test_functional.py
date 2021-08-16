import allure
from framework.browser.browser import Browser
from tests.pages.login_end_interes_page import LoginAndInteresPage
from framework.utils.logger import Logger


class TestFunctional(object):
    def test_case_1(self, create_browser):
        Logger.info('Test Case №1')
        with allure.step("First step"):
            Browser.get_browser().set_url('https://userinyerface.com/game')
            page = LoginAndInteresPage()
            assert page, 'Страница открылась или не корректно или это не она!'

            assert page.is_autorization_form_displayed(), (
                   "Не отображается форма регистрации\
                    или мы на другой странице")

            password = 'Silverwan1ы'
            email = 'aka'
            domain = 'Setras'
            assert page.login(password, email, domain), (
                "Не отображается форма заполнения информации\
                 или мы на другой странице"
            )
            assert page.select_int_and_upload_img(), (
                "Не отображается форма персональной информации\
                 или мы на другой странице"  
            )
    
    def test_case_2(self, create_browser):
        Logger.info('Test Case №2')
        with allure.step("Second step"):
            Browser.get_browser().set_url('https://userinyerface.com/game')
            page = LoginAndInteresPage()
            assert page, 'Страница открылась или не корректно или это не она!'
            assert page.help_window_must_be_hidden(), 'Страница открылась или не корректно или это не она!'


    def test_case_3(self, create_browser):
         Logger.info('Test Case №2')
         with allure.step("Tird step"):
             Browser.get_browser().set_url('https://userinyerface.com/game')
             page = LoginAndInteresPage()
             assert page, 'Страница открылась или не корректно или это не она!'
             assert page.accept_cookie(), 'Форма с куками не пропала'

    def test_case_4(self, create_browser):
        Logger.info('Test Case №2')
        with allure.step("Tird step"):
             Browser.get_browser().set_url('https://userinyerface.com/game')
             page = LoginAndInteresPage()
             assert page, 'Страница открылась или не корректно или это не она!'
             assert page.check_timer_starts_from_zero(), 'Таймер начался не с нуля'