import pytest
import allure
from _pytest.runner import runtestprotocol

from framework.browser.browser import Browser
from framework.database.db_utils import DB_Utils
from framework.utils.logger import Logger

from tests.MyUtils.other_utils import MyUtils
from tests.DB_models.Table_test import Table_test

from tests.config.browser import Grid
from tests.config.test_data.t_data import TableTestData
from tests.config.browser import BrowserConfig

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default=BrowserConfig.BROWSER,
                     help="Name of browser")
    parser.addoption("--grid_port", action="store", default=Grid.GRID_PORT,
                     help="Port of remote connection")

@pytest.fixture(scope="session")
def create_browser(request):
    """
        Создание сессии браузера с именем из конфиг файла.
    Args:
    """
    Logger.info("Создание сессии браузера из конфиг файла"):
    browser = request.config.getoption('--browser')
    Browser.get_browser().set_up_driver(browser_key=browser, grid_port=request.config.getoption('--grid_port'))
    Browser.get_browser().maximize(browser_key=browser)

    yield

    Logger.info("Закрытие сессий всех браузеров"):
    for browser_key in list(Browser.get_browser().get_driver_names()):
        Browser.get_browser().quit(browser_key=browser_key)

def pytest_runtest_protocol(item, log=True, nextitem=None):
    # Provide's test case execution details
    reports = runtestprotocol(item, nextitem=nextitem)
    for report in reports:
        if report.when == 'call':
            # get test case name and test case status
            Logger.info('\n%s --- %s' % (item.name, report.outcome))
    return True

@pytest.fixture(scope='function')
def write_test_result_in_db(method, request):
    Logger.info('Создаём экземпляр модели таблицы')
    table = Table_test(tb_name=TableTestData.table_name)
    Logger.info(f'Получаем имя текущего теста')
    name = str(request.node.name).split('[')[0]
    Logger.info(f'Имя текущего теста= {name}')
    start_time = MyUtils.convert_to_datatime()[0]
    yield
    if pytest_runtest_protocol(item=request.node):
        status_id = TableTestData.status_passed
    else:
        status_id = TableTestData.status_passed 
    end_time = MyUtils.convert_to_datatime()[1]
    browser = BrowserConfig.BROWSER   
    Logger.info('Формируем словарь собранных из теста и из конфигурации данных')
    table_data = {"name": name,"status_id": status_id, 
                      "method_name": method,
                      "project_id":TableTestData.project_name, "session_id":TableTestData.session_data, 
                      "start_time":start_time, "end_time":end_time,
                      "env":TableTestData.env, "browser":browser, "author_id":TableTestData.author_data}
    conn = table.conn
    table.check_update_and_add_entry(table_data=table_data, conn=conn)

@pytest.fixture
def test_simulate(request, connect, table):
    Logger.info('Копируем тест')
    id = request.param
    Logger.info(f'Параметры request {id}')
    copied_test = table.get( conn=connect, column_name='*', 
                                condition=f"id = {id}")
    Logger.info(f'Текущее соединение {connect}')
    Logger.info(f'Скопированный тест {copied_test}')
    yield copied_test
    Logger.info('Удаляем тест после изменения')
    table.delete_entry_in_table(conn=connect, condition=f'id = {request.param}')