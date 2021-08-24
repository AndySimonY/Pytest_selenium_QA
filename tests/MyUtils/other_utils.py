import os
import cv2
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

    @staticmethod
    def calc_image_hash(FileName):
        image = cv2.imread(FileName) #Прочитаем картинку
        resized = cv2.resize(image, (8,8), interpolation = cv2.INTER_AREA) #Уменьшим картинку
        gray_image = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY) #Переведем в черно-белый формат
        avg=gray_image.mean() #Среднее значение пикселя
        ret, threshold_image = cv2.threshold(gray_image, avg, 255, 0) #Бинаризация по порогу
        
        #Рассчитаем хэш
        _hash=""
        for x in range(8):
            for y in range(8):
                val=threshold_image[x,y]
                if val==255:
                    _hash=_hash+"1"
                else:
                    _hash=_hash+"0"
                
        return _hash

    @staticmethod
    def compare_hash(hash1,hash2):
        l=len(hash1)
        i=0
        count=0
        while i<l:
            if hash1[i]!=hash2[i]:
                count=count+1
            i=i+1
        return count    

    @staticmethod
    def get_comparison_result(image_1_path, image_2_path):
        hash1=MyUtils.calc_image_hash(os.getcwd() + image_1_path)
        hash2=MyUtils.calc_image_hash(os.getcwd() + image_2_path)
        result = MyUtils.compare_hash(hash1, hash2)
        return result


