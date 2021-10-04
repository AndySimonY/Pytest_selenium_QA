from framework.jsonUtils.json_converter import JsonConverter
from framework.utils.logger import Logger

class StepTests:

     @staticmethod
     def books_is_sort_by_id_step_1(books):
        books_list = books.catalog.book
        id_with_letter = list(map(lambda x: x.id, books_list))
        ids = []
        for id in id_with_letter:
            ids.append(''.join(filter(lambda x: x.isdigit(), id)))
        return ids == sorted(ids)

     @staticmethod
     def book_min_max_price_is_not_equal_step_2(books):
        result = False
        books_list = books.catalog.book
        book_min_price = JsonConverter.json_converter([{
                        "title":i.title, "description":i.description, "price":i.price} 
                        for i in books_list if i.price == min(
                        list(map(lambda x: x.price, books_list)), 
                        key= lambda i: float(i))])
        book_max_price = JsonConverter.json_converter([{
                        "title":i.title, "description":i.description, "price":i.price} 
                        for i in books_list if i.price == max(
                        list(map(lambda x: x.price, books_list)), 
                        key= lambda i: float(i))])
        Logger.info(f"Проверка объектов книг с минимальной ценой - {book_min_price} и \
            максимальной ценой - {book_max_price} на идентичность")
        if len(book_min_price) >= len(book_max_price):
            for min_book in book_min_price:
                for max_book in book_max_price:
                    if max_book is not min_book:
                        result = True
                    else:
                        result=False
                        break
        else:
            for max_book in book_max_price :
                for min_book in book_min_price:
                    if max_book is not min_book:
                        result = True
                    else:
                        result=False
                        break
        return result