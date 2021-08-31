from framework.utils.logger import Logger
from framework.database.db_utils import DB_Utils
from tests.MyUtils.other_utils import MyUtils

class Table_test(DB_Utils):

    def __init__(self, tb_name):
        super().__init__(tb_name)
    
    def insert_test_table_data(self, 
                               name, status_id,
                               method_name,project_data, 
                               session_data, start_time, 
                               end_time, env, 
                               browser, author_data):
        if status_id == False:
            status_id = 'FAILED'
        elif status_id == True:
            status_id = 'PASSED'
        else:
            status_id = 'SKIPPED'
        Logger.info(f"Устанавливаем статус теста {status_id}")
        table_data = {"name": name,"status_id": status_id, 
                      "method_name": method_name,
                      "project_id":project_data, "session_id":session_data, 
                      "start_time":start_time, "end_time":end_time,
                      "env":env, "browser":browser, "author_id":author_data} # Формируем словарь для дальнейшей обработки
        self.chek_update_and_add_entry(table_data=table_data) # добавляем недостающие данные в связанные таблицы, а затем добавим данные в целевую

    def simulate_and_update_test(self, simulate_data):
        try:
            Logger.info('Симулируем выполнение тест')
            Logger.info('Выбираем тесты со случайно повторяющимися id на подобие "77"')
            id = MyUtils.generate_from_to_numbers(count=1, start=1, end=9, duplicate=True)[0]
            Logger.info(f'Получаем запись теста из DB по id {id}')
            copied_test = self.get(column_name='*', table_name='test',condition=f'id = {id}')
            self.chek_update_and_add_entry(table_data=simulate_data, 
                                           condition=f'id = {id}', 
                                           update_flag=True)
            self.delete_entry_in_table(condition=f'id = {id}')
            return True
        except RuntimeError as e:
            return e