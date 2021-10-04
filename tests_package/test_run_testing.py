"""Test dependencies"""
import pytest

"""API instance"""
from config.apiMethods.api_utils import ApiUtils

"""Config data"""
from config.api_config.api_headers import BASE_HEADER
from config.api_config.api_urls import Urls

"""Test methods"""
from tests_package.step_tests import StepTests

"""Logs"""
from framework.utils.logger import Logger

class TestFunctional(object):

      @pytest.mark.parametrize("base_url", [(Urls.BASE_URL)])
      def test_books_api(self, base_url):
          api = ApiUtils(headers=BASE_HEADER)

          Logger.info("STEP ONE")
          books = api.get_books(url=base_url)
          assert StepTests.books_is_sort_by_id_step_1(books), "Книги отсортированы не по позрастанию id"

          Logger.info("STEP TWO")
          assert StepTests.book_min_max_price_is_not_equal_step_2(books), "Все, либо некоторые\
              из книг идентичны между представленных с минимальной и максимально ценой"