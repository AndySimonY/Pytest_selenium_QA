import pytest
from tests.config.wait_after_request import Wait
from framework.utils.logger import Logger
import time


@pytest.fixture(scope="function")
def wait_for_next_request(request):
    yield
    time.sleep(Wait.WAIT_AFTER_REQUEST)
    Logger.info('Ожидание')