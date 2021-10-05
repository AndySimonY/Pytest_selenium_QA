import pytest
from framework.utils.logger import Logger
from framework.browser.browser import Browser
from tests_package.config.browser import BrowserConfig
from tests_package.config.browser import Grid
from datetime import datetime

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
    Logger.info("Создание сессии браузера из конфиг файла")
    browser = request.config.getoption('--browser')
    Browser.get_browser().set_up_driver(browser_key=browser, grid_port=request.config.getoption('--grid_port'))
    Browser.get_browser().maximize(browser_key=browser)

    yield

    # Logger.info("Закрытие сессий всех браузеров")
    # for browser_key in list(Browser.get_browser().get_driver_names()):
    #     Browser.get_browser().quit(browser_key=browser_key)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    try:
        Logger.info('Создаём скриншот неудачного UI теста')
        outcome = yield
        rep = outcome.get_result()
        if rep.when == 'call' and rep.failed:
            now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            Browser().get_driver().save_screenshot(f".\screenshots\{now}.png")
    except:
        pass