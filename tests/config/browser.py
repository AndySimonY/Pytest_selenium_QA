import os


class BrowserConfig(object):
    # Настройки браузера
    # Поддерживаемые браузеры: "chrome", "firefox"
    BrowserSettings = 'IDEA' # 'JENKINS' or 'IDEA'
    if BrowserSettings == 'JENKINS':
        BROWSER = os.getenv('browser')
        CHROME_VERSION = os.getenv('chrome_version')
        FIREFOX_VERSION = os.getenv('firefox_version')
        LANGUAGE = os.getenv('language')
    elif BrowserSettings == 'IDEA':
        BROWSER = 'chrome'
        CHROME_VERSION = '75.0'
        FIREFOX_VERSION = '66.0'
        LANGUAGE = 'ru'

class Grid(object):
    USE_GRID = False
    GRID_HOST = "localhost"
    GRID_PORT = "5565"
    GRID_URL = "http://{host}:{port}/wd/hub"
    # .format(host=GRID_HOST, port=GRID_PORT)
    IS_VNC_ENABLED = True
    IS_VIDEO_ENABLED = False
