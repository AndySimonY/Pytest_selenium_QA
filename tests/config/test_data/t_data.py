from datetime import datetime as dtime
from tests.MyUtils.other_utils import MyUtils
from enum import Enum

"""Общие тестовые данные"""
class Tdata(Enum):
    password = 'Silverwan1ы'
    email = 'aka'
    domain = 'Setras'

"""Тестовые данные только для таблицы test"""
class TableTestData():

      table_columns = ('name', 'status_id', 'method_name',\
                'project_id', 'session_id', 'start_time', 'end_time',\
                'env', 'browser', 'author_id')

      author_data = {"name":'Andranik', "login":'Andy', "email":'aro.vov@yandex.ru'}
      project_name = {"name":'DBask'}
      session_data = {"session_key":'1476344018022', 
                      "created_time":MyUtils.convert_to_datatime()[0],
                      "build_number":'5'} # измените ключ ссессии если требуется
      env = 'SimonyanA'
      status = ['PASSED', 'FAILED']

      test_simulate_id = MyUtils.generate_from_to_numbers(count=1,  # Измените данное значение если хотите симулировать другое количесво тестов
                                                  start=1, 
                                                  end=9, 
                                                  duplicate=True) 
      table_column_for_update = ('status_id','project_id','start_time','end_time')# Колонки, которые мы изменяем, когда симулируем выполнение тестов

      # Уникальные данные теста №1 для таблицы test
      method_name_for_test_1 = 'userinyerface.com.tests.MakeSureThatTheHelpWindowIsHidden'

      # Уникальные данные теста №1 для таблицы test
      method_name_for_test_2 = 'userinyerface.com.TheCookieAcceptanceWindowShouldDisappear'