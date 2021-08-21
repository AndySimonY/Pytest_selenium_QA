from framework.api.base_api import BaseApi
from framework.api.json_converter import JsonConverter

from routes.VKApiUtils import VKApiUtils

from tests.other_utils import MyUtils


class VKApi(BaseApi):

    def __init__(self, headers, access_tocken):
        self.apivk = VKApiUtils(headers, access_tocken)
        super.__init__(headers)

    # def get_response_obj(self, url, query = '', status = 200, Class=None):
    #     response = self.get(MyUtils.join_path(url) + query)
    #     assert response.status_code == 200, 'Запрос провалился'
    #     json_obj = JsonConverter.get_json(response)
    #     assert json_obj, "Кажется это не JSON формат"
    #     return JsonConverter.json_converter(json_obj, Class=Class)

    def create_post_on_my_page(self, params=[]):
        create_entry = self.apivk.wall_post(params=params)
        assert create_entry.status_code == 200, "Ошибка при отправке запроса"

    def edit_post_on_my_page(self, group_id, filepath):
        upload_url = self.apivk.getWallUploadServer(group_id)['response']['upload_url'] # Можно конечно этот ответ конвертировать в класс, 
        file_inf = self.post(upload_url, files=MyUtils.file(filepath=filepath)).json()         # но ради одного урла, возможно, это не имеет смысла
        save_wall_photo = self.apivk.saveWallPhoto()