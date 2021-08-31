import allure
import pytest
from datetime import datetime as dtime

from framework.browser.browser import Browser
from framework.utils.logger import Logger

from tests.pages.login_page import LoginPage
from tests.DB_models.Table_test import Table_test

from tests.config.test_data.urls import Urls
from tests.config.browser import BrowserConfig
from tests.config.test_data.t_data import TableTestData


from tests.MyUtils.other_utils import MyUtils

class TestFunctional(object):
    
    @pytest.mark.parametrize('target_table', [('test')])
    def test_case_1(self,target_table, create_browser):
       start_time = dtime.now()
       table = Table_test(tb_name=target_table)

       Logger.info(f"Перейти на сайт по ссылке {Urls.BASE_URL}")
       Browser.get_browser().set_url(Urls.BASE_URL)
       page = LoginPage()
       assert page, 'Страница открылась или не корректно, или это не она!'

       Logger.info("Скрыть окно форму 'Help'")
       page.is_autorization_form_displayed()
       page.click_close_help_window_buttom()
       status = page.get_class_style_of_help_window()
       start_time, end_time = MyUtils.convert_to_datatime(start_time)
       table.insert_test_table_data(
                    name=TableTestData.name_for_test_1, status_id=status,
                    method_name=TableTestData.method_name_for_test_1,
                    project_data=TableTestData.project_name, session_data=TableTestData.session_data,
                    start_time=start_time, end_time=end_time, env=TableTestData.env,
                    browser=BrowserConfig.BROWSER, author_data=TableTestData.author_data)
       assert status, (
                     'Страница открылась или не корректно или это не она!')

    @pytest.mark.parametrize('target_table', [('test')])
    def test_case_2(self, target_table,create_browser):
         start_time = dtime.now()
         table = Table_test(tb_name=target_table)

         Logger.info(f"Перейти на сайт по ссылке {Urls.BASE_URL}")
         Browser.get_browser().set_url(Urls.BASE_URL)
         page = LoginPage()
         assert page, 'Страница открылась или не корректно или это не она!'

         Logger.info("Принять использование cookie")
         page.is_autorization_form_displayed()
         page.click_button_accept_cookie()
         status = page.is_invisibility_cookie_form()
         start_time, end_time = MyUtils.convert_to_datatime(start_time)
         table.insert_test_table_data(
                    name=TableTestData.name_for_test_2, status_id=status,
                    method_name=TableTestData.method_name_for_test_2,
                    project_data=TableTestData.project_name, session_data=TableTestData.session_data,
                    start_time=start_time, end_time=end_time, env=TableTestData.env,
                    browser=BrowserConfig.BROWSER, author_data=TableTestData.author_data)
         assert status, 'Форма с куками не пропала'

    @pytest.mark.parametrize('simulate_data', 
    [(
           {'status_id':'PASSED', 'project_id':TableTestData.project_name, 'end_time':MyUtils.convert_to_datatime()[1]})
    ])
    def test_case_3(self, simulate_data):
           Logger('Симуляция выполнения 1 теста')
           table = Table_test(tb_name='test')
           assert table.simulate_and_update_test(simulate_data=simulate_data)
    
    @pytest.mark.parametrize('simulate_data', 
    [(
           {'status_id':'FAILED', 'project_id':TableTestData.project_name, 'browser': 'edge'})
    ])
    def test_case_4(self, simulate_data):
           Logger('Симуляция выполнения 2 теста')
           table = Table_test(tb_name='test')
           assert table.simulate_and_update_test(simulate_data=simulate_data)


    @pytest.mark.parametrize('simulate_data', 
    [(
           {'status_id':{'name': 'PASSED'}, 'project_id':TableTestData.project_name, 'author_id':TableTestData.author_data})
    ])
    def test_case_5(self, simulate_data):
           Logger('Симуляция выполнения 3 теста')
           table = Table_test(tb_name='test')
           assert table.simulate_and_update_test(simulate_data=simulate_data)