import os
import random
import string
from tests.config.test_data.urls import Urls

class MyUtils:
    
    @staticmethod
    def get_id_list(lis):
        try:
            new_list = []
            for i in lis:
                new_list.append(i.id)
            return new_list
        except ValueError as e:
            return e

    @staticmethod
    def generate_random_text(length):
            letters = list(string.ascii_letters)
            rand_str = ''
            for i in range(length):
                rand_str = rand_str + ''.join(random.choice(letters))
            return rand_str

    @staticmethod
    def join_path(path, host = Urls.BASE_URL_API):
            host_path = host + path
            return host_path

    @staticmethod
    def file(filepath=''):
        """Указать путь к файлу относительно рабочей директории"""
        files = {"file": open(os.getcwd() + filepath, "rb")}
        return files