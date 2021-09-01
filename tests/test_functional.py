import time
import random
import pytest
from datetime import datetime as dtime

from framework.browser.browser import Browser
from framework.database.db_utils import DB_Utils
from framework.jsonUtils.json_converter import JsonConverter
from framework.utils.logger import Logger

from tests.pages.login_page import LoginPage
from tests.DB_models.Table_test import Table_test

from tests.config.test_data.urls import Urls
from tests.config.browser import BrowserConfig
from tests.config.test_data.t_data import TableTestData


from tests.MyUtils.other_utils import MyUtils

class TestFunctional(object):

      connect = DB_Utils.connect()
      table_test = Table_test(tb_name='test')
       
      @pytest.mark.parametrize('method', [(TableTestData.method_name_for_test_1)])
      def test_hidden_help_window(self, write_test_result_in_db, create_browser):

              Logger.info(f"Перейти на сайт по ссылке {Urls.BASE_URL}")
              Browser.get_browser().set_url(Urls.BASE_URL)
              page = LoginPage()
              assert page, 'Страница открылась или не корректно, или это не она!'

              Logger.info("Скрыть окно форму 'Help'")
              page.is_autorization_form_displayed()
              page.click_close_help_window_buttom()
              assert page.get_class_style_of_help_window(), (
                     'Страница открылась или не корректно или это не она!')
    
      @pytest.mark.parametrize('method', [(TableTestData.method_name_for_test_2)])
      def test_case_accept_coocie(self,write_test_result_in_db, create_browser):
         Logger.info(f"Перейти на сайт по ссылке {Urls.BASE_URL}")
         Browser.get_browser().set_url(Urls.BASE_URL)
         page = LoginPage()
         assert page, 'Страница открылась или не корректно или это не она!'

         Logger.info("Принять использование cookie")
         page.is_autorization_form_displayed()
         page.click_button_accept_cookie()
         assert page.is_invisibility_cookie_form(), 'Форма с куками не пропала'

      @pytest.mark.parametrize("connect, table", [(connect, table_test)])
      @pytest.mark.parametrize("test_simulate", TableTestData.test_simulate_id, 
                                                  indirect=True)
      @pytest.mark.parametrize("update_test_data, status_passed", [({
              'status_id': random.choice(TableTestData.status), 'project_id':TableTestData.project_name, 'end_time':MyUtils.convert_to_datatime()[1]
                     }, 'PASSED')]
              )
      def test_simulating(self, update_test_data, status_passed, test_simulate):
              update_test_data = JsonConverter.json_converter(update_test_data)
              waiting = MyUtils.generate_from_to_numbers(count=1, start=0, end=2)
              time.sleep(waiting)
              self.table_test.check_update_and_add_entry(conn=self.connect, 
                                                         table_data=update_test_data,
                                                         condition=f'id = {test_simulate[0]}', 
                                                         update_flag=True)
              update_test_data.status_id = random.choice(TableTestData.status)
              if update_test_data.status_id == status_passed:
                     assert True
              else:
                     assert False