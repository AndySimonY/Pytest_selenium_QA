from tests.config.test_data.urls import Urls
from tests.config.test_data.t_data import Tdata
import requests
from framework.api.json_converter import JsonConverter
from tests.other_utils import MyUtils
from tests.config.test_data.api_headers import RequestHeaders

headers = RequestHeaders.BASE_HEADERS

def generate_request_vkapi(method,  token = Tdata.ACCESS_TOKEN, version = Tdata.VERSION,
                               params=[], url = Urls.BASE_URL_API):            
    if len(params) > 1:
            params_query = ''
            for p in params:
                params_query += p + '&'
            return url + method + '?' + params_query + token + '&' + version      
    elif len(params) == 1:
            return url + method + '?' + params[0] + '&' + token + '&' + version
    else:
            return url + method + '?' + token + '&' + version

urls = url=generate_request_vkapi('photos.getWallUploadServer', params=['group_id=532457467'])

def wall_post(urls ,headers):
    request = requests.post(urls, headers)
    return request

url_upload_img = wall_post(urls, headers).json()['response']['upload_url']
# print(wall_post(urls, headers).json()['response']['upload_url'])

upload_img = requests.post(url_upload_img, files=MyUtils.file(filepath='\\tests\config\\test_data\img\image.jpg'))
upload_img_json = JsonConverter.get_json(upload_img)
print(JsonConverter.json_converter(upload_img_json))