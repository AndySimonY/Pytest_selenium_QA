from framework.utils.logger import Logger
from framework.database.db_utils import DB_Utils
from tests.MyUtils.other_utils import MyUtils

class Table_test(DB_Utils):

    def __init__(self, tb_name):
        self.conn = self.connect()
        super().__init__(tb_name)