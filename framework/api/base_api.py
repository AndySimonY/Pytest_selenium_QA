import requests
from framework.utils.logger import Logger

class BaseApi:

    _r = requests.session()
    
    def __init__(self, headers):
       self.headers = headers

    def get(self, url):
        Logger.info("Отправка запроса get по пути " + url)
        result = requests.get(url, headers = self.headers)
        return result

    def post(self, url, body='', files=None, **kwargs):
        try:
            Logger.info("Отправка запроса post по пути " + url)
            if files:
                result = self._r.post(url,
                                json=body,
                                headers=self.headers, 
                                **kwargs)
            else:
                result = self._r.post(url,
                                files=body,
                                headers=self.headers
                                **kwargs)
            return result
        except:
            Logger.info("Произошла ошибка во время отпрваки post запроса")
       
    def delete(self, url):
        Logger.info("Отправка запроса delete по пути " + url)
        result = self._r.delete(url, headers=self.headers)
        return result