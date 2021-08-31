import mysql.connector
from mysql.connector import Error
from tests.config.local import DB_settings
from framework.utils.logger import Logger
from framework.api.json_converter import JsonConverter
 
class DB_Utils():

    def __init__(self, tb_name):
        self.tb_name = tb_name
        
    def connect(self):
        try:
            Logger.info(f"Подключаемся к базе данных {self.tb_name}")
            conn = mysql.connector.connect(
                host=DB_settings.host,
                database=DB_settings.database,
                user=DB_settings.username,
                password=DB_settings.password,
                port=DB_settings.port
            )
            Logger.info("Успешно подключено")
            return conn
        except(Exception, Error) as error:
            return error

    def insert_in_table(self, table_data, table_name='',table_column=(),):
        with self.connect() as conn:
            cursor = conn.cursor()
            if not table_name:
                table_name= self.tb_name
            Logger.info(f'Запись данных {table_data} в таблицу {table_name}')
            if isinstance(table_data, dict):
               key_data, value_data = JsonConverter.dict_iterator_get_keys_and_val(table_data)
               table_data = tuple(value_data)
               query_dat_col = self.convert_to_valid_col(key_data)
               query = f"""INSERT INTO {table_name} ({query_dat_col}) VALUES {table_data}"""
               try:
                    Logger.info(f"Отправка запроса {query}")
                    cursor.execute(query)
               except:
                    raise 'Произошла ошибка во время запроса'
               conn.commit()
            elif isinstance(table_column, tuple) and isinstance(table_data, tuple):
                """Обрабатывается из метода  chek_and_add_entry"""
                query_dat_col = self.convert_to_valid_col(table_column)
                query = f"""INSERT INTO {table_name} ({query_dat_col}) VALUES {table_data}"""
            else:   
                query = f"""INSERT INTO {table_name} ({table_column}) VALUES ('{table_data}')"""
            try:
                    Logger.info(f"Отправка запроса {query}")
                    cursor.execute(query)
            except:
                    raise f'Произошла ошибка во время запроса'
            conn.commit()

    def get(self, column_name, table_name='', condition=''):
                if not table_name:
                    table_name = self.tb_name
                with self.connect() as conn:
                        cursor = conn.cursor()
                        if condition:
                                query = f"""SELECT {column_name} FROM {table_name} WHERE {condition}"""
                                Logger.info(f'Получаем запись в таблице {table_name}\
                                по условию {condition}, по запросу {query}')
                                for res in cursor:
                                    if len(res) == 1:
                                        return res[0]
                                    return res
                        else:
                                resp = []
                                query = f"""SELECT {column_name} FROM {table_name}"""
                                Logger.info(f'Получаем запись в таблице {table_name}\
                                , по запросу {query}')
                        try:
                                cursor.execute(query)
                                for res in cursor:
                                    resp.append(res)
                                return resp
                        except RuntimeError as error:
                                return error

    def chek_update_and_add_entry(self, table_data, 
                           update_flag=False,
                           condition=''):
        """Метод добавляет недостающую информацию в связанные 
           с целевой таблицей таблицы, а после, достаёт id уже 
           добавленных значений и вставляет запись в целевую таблицу. 
           Чтобы функция работала корректно ей необходимо передать данные в виде словаря ключ-значение
           (колонка-значение), но также возможно передать просто строку как
           значение, тогда для нее будте рассмотренна колонка name.
           Также функция способна обновить данные, предварительно проверив
           все доступные внешние ключи, важное условие - внешний ключ должен 
           содержать _id, хотя если будет нужно это тоже можно добавить в параметры"""
        with self.connect() as conn:
                cursor = conn.cursor()
                columns = []
                Logger.info('Запущена функция проверки и добавления недостающих данных')
                if not update_flag:
                   columns = self.get_table_all_columns(table_name=self.tb_name)
                else:
                    columns = JsonConverter.get_keys(table_data)
                Logger.info(f'Колонки целевой таблицы {columns}')
                for q in columns:
                        col = str(q)
                        if col.find('_id') != -1:
                            table = col.replace('_id', '')
                            Logger.info(f"Таблицы для проверки {table}")
                            data_quer = table_data[col]
                            if isinstance(data_quer, dict):
                                test_data_key, test_data_val = JsonConverter.dict_iterator_get_keys_and_val(
                                                                        table_data[col]) 
                                subQuery = self.create_long_condition(key=test_data_key, val=test_data_val)
                                query = f"""SELECT EXISTS(SELECT id FROM {table} WHERE {subQuery})"""
                            else:
                                subQuery=f"name='{data_quer}'"
                                query = f"""SELECT EXISTS(SELECT id FROM {table} WHERE {subQuery})"""
                            cursor = conn.cursor()
                            Logger.info(f'Отправка запроса на проверку наличия записи в таблице {table} \
                                и телом запроса {query}')
                            cursor.execute(query)
                            for que in cursor:
                                stat_q = que[0]  
                            if stat_q == 1:
                                table_id = self.get(table_name=table,
                                                  condition=subQuery,
                                                  column_name='id')
                                table_data[col] = table_id
                            else:
                                other_table_col = []
                                cursor.execute(f"SHOW COLUMNS FROM {table}")
                                for c in cursor:
                                    if c[0] != 'id':
                                        other_table_col.append(c[0])
                                Logger.info(f'Колонки {other_table_col} таблицы {table}')
                                if isinstance(data_quer, dict):
                                    self.insert_in_table(
                                        table_column=tuple(other_table_col),
                                        table_data=tuple(test_data_val), table_name=table)
                                    table_id = self.get(table_name=table,
                                                        condition=subQuery, 
                                                        column_name='id')
                                    table_data[col] = table_id  
                                else:
                                    self.insert_in_table(
                                        table_column=''.join(other_table_col),
                                        table_data=''.join(data_quer), )
                                    table_id = self.get(table_name=table,
                                                        condition=subQuery)
                                    table_data[col] = table_id
                try:
                    if not update_flag:
                        Logger.info(f"Запись данных в целевую таблицу {self.tb_name}")
                        self.insert_in_table(table_column=columns,table_data=table_data, table_name=self.tb_name)
                    else:
                         Logger.info(f"Обновляем данные в целевой таблице {self.tb_name}")
                         self.update_data_in_table(update_table_col=table_data, condition=condition)
                except:
                    raise RuntimeError('Функция упала с ошибкой, пожалуйстра проверьте входные данные')

    def update_data_in_table(self, update_table_col, 
                         condition, table_name=''):
        if not table_name:
            table_name = self.tb_name
        if isinstance(update_table_col, dict):
            update_table_col = self.create_long_condition(update_table_col,
                                                          update_flag=True)
        with self.connect() as conn:
                cursor = conn.cursor()
                query = f"""UPDATE {table_name} SET {update_table_col} WHERE {condition}"""
                Logger.info(f'Обнавляем запись в таблице {table_name}\
                    по условию {condition}, по запросу {query}')
                try:
                    cursor.execute(query)
                    conn.commit()
                except:
                    raise RuntimeError('Функция обновления не выполнилась, проверьте тестовые данные')

    def delete_entry_in_table(self, table_name='', condition=''):
        with self.connect() as conn:
            if not table_name:
                table_name = self.tb_name
                cursor = conn.cursor()
                if condition:
                     Logger.info('Удаляем данные из таблицы {table_name} по условию {condition}')
                     query = f"""DELETE FROM {table_name} WHERE {condition}"""
                else:
                    Logger.info('Удаляем все данные из таблицы {table_name}')
                    reserve_data = self.get(column_name='*')
                    with open(f"deleted_table_data.py", 'a+') as reserve:
                        reserve.write(reserve_data)
                    query =  f"""DELETE FROM {table_name}"""
                    Logger.info(f'Отправляем запрос на удаление {query}')
                try:
                    cursor.execute(query)
                    conn.commit()
                except:
                    raise RuntimeError('Функция удаления не выполнилась, проверьте входные данные')

    def get_table_all_columns(self, table_name=''):
        if not table_name:
            table_name = self.tb_name
        with self.connect() as conn:
                cursor = conn.cursor()
                columns = []
                cursor.execute(f"SHOW COLUMNS FROM {table_name}")
                for column in cursor:
                        columns.append(column[0])
                return columns           

    @staticmethod
    def convert_to_valid_col(table_column):
                query_dat_col = ''
                for d in table_column:
                    if isinstance(d, str):
                        st = d.replace("'", "")
                        query_dat_col += st + ','
                query_dat_col = query_dat_col[:-1]
                return query_dat_col

    @staticmethod
    def create_long_condition(colums_key_val_dict={},key='', 
                              val='', update_flag=False):
                        if colums_key_val_dict:
                            key, val = JsonConverter.dict_iterator_get_keys_and_val(colums_key_val_dict)
                        subQuery = ''
                        for i in range(len(val)):
                            st = val[i]
                            if len(val) - i == 1:
                                subQuery+= f'{key[i]}="{st}"'
                            elif update_flag: # Подойдёт для павильного обображения колонок в запросе UPDATE
                                subQuery+= f'{key[i]}="{st}", '
                            else:
                                subQuery+= f'{key[i]}="{st}" AND '
                        Logger.info(f'Подзапрос {subQuery}')
                        return subQuery