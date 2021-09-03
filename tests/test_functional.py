import pytest
from framework.browser.browser import Browser
from tests.config.urls import Urls
from tests.pages.login_page import LoginPage
from framework.utils.logger import Logger
from tests.pages.welcome_page import WelcomePage
from tests.pages.filling_inf_page import FillingInfPage


class TestFunctional(object):
        
    def test_case_2(self, create_browser):
            Logger.info("First step")
            Browser.get_browser().set_url(Urls.TEST_STAND_URL)
            page = LoginPage()
            assert page, 'Страница открылась или не корректно, или это не она!'
            Logger.info("Second step")
            page.is_autorization_form_displayed()
            page.click_close_help_window_buttom()
            assert  page.get_class_style_of_help_window(), 'Страница открылась или не корректно или это не она!'


    @pytest.mark.parametrize('time_start_with', [('00:00:00')])
    def test_case_4(self,time_start_with, create_browser):
             Logger.info("Tird step")
             Browser.get_browser().set_url(Urls.TEST_STAND_URL)
             page = LoginPage()
             assert page, 'Страница открылась или не корректно или это не она!'
             page.is_autorization_form_displayed()
             assert page.is_timer_started_of_the_time(time_start_with), 'Таймер начался не с нуля'