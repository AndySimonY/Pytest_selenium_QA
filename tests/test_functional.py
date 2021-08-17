import os
import allure
import pytest
from framework.browser.browser import Browser
from tests.config.urls import Urls
from tests.pages.login_page import LoginPage
from tests.pages.welcome_page import WelcomePage
from tests.pages.filling_inf_page import FillingInfPage


class TestFunctional(object):
    
    @pytest.mark.parametrize('password, email, domain, index_for_unsellect_all, \
                              no_select_interes_name, file_path',
                              [('Silverwan1ы', 'aka', 'Setras', 20, 
                              'Select all', Urls.PATH_FOR_IMAGE_AVA)])
    def test_case_1(self, password, 
                    email, domain, index_for_unsellect_all,
                    no_select_interes_name, file_path, create_browser):
        with allure.step("First step"):
            Browser.get_browser().set_url(Urls.TEST_STAND_URL)
            page = WelcomePage()
            assert page, 'Страница открылась или не корректно, или это не она!'
        with allure.step("Second step"):
            page = LoginPage()
            assert page.is_autorization_form_displayed(), (
                   "Не отображается форма регистрации\
                    или мы на другой странице")
        with allure.step("Tird step"):
            page.clear_field_password__and_send_keys(password)
            page.clear_field_email__and_send_keys(email)
            page.clear_field_domain__and_send_keys(domain)
            page.selec_dropdown_item()
            page.uncheck_politic()
            assert page.inf_fields_is_displayed(), (
                "Не отображается форма заполнения информации\
                 или мы на другой странице")
        with allure.step("Fourth step"):
            page = FillingInfPage()
            items = page.get_checkbox_items()
            page.click_unselect_all(index_for_unsellect_all, items)
            for el in range(len(items)):
                elem = -1
                if items[el].text == no_select_interes_name:
                    elem = el
                    break
            page.select_random_interes(4, items, elem)
            page.upload_image(file_path)
            page.click_next_button()
            assert page.is_displaeyd_following_person_inf(), (
                "Не отображается форма персональной информации\
                 или мы на другой странице")
    
    def test_case_2(self, create_browser):
        with allure.step("First step"):
            Browser.get_browser().set_url(Urls.TEST_STAND_URL)
            page = LoginPage()
            assert page, 'Страница открылась или не корректно, или это не она!'
            with allure.step("Second step"):
                page.is_autorization_form_displayed()
                page.click_close_help_window_buttom()
                assert page.get_class_style_of_help_window(), 'Страница открылась или не корректно или это не она!'

    def test_case_3(self, create_browser):
         with allure.step("Tird step"):
             Browser.get_browser().set_url(Urls.TEST_STAND_URL)
             page = LoginPage()
             assert page, 'Страница открылась или не корректно или это не она!'
             with allure.step("Second step"):
                page.is_autorization_form_displayed()
                page.click_button_accept_cookie()
                assert page.is_invisibility_cookie_form(), 'Форма с куками не пропала'

    @pytest.mark.parametrize('time_start_with', [('00:00:00')])
    def test_case_4(self,time_start_with, create_browser):
        with allure.step("Tird step"):
             Browser.get_browser().set_url(Urls.TEST_STAND_URL)
             page = LoginPage()
             assert page, 'Страница открылась или не корректно или это не она!'
             page.is_autorization_form_displayed()
             assert page.is_timer_started_of_the_time(time_start_with), 'Таймер начался не с нуля'