from framework.utils.logger import Logger
from framework.api.json_converter import JsonConverter

from tests.routes.VKApiUtils import VKApiUtils

from tests.other_utils import MyUtils

class VKApi:

    def __init__(self, headers, access_tocken):
        self.apivk = VKApiUtils(headers, 
                                access_tocken)

    def create_post_on_my_page(self, params=[]):
        create_entry = self.apivk.wall_post(params=params)
        assert create_entry.status_code == 200, "Ошибка при отправке запроса"
        return JsonConverter.json_converter(create_entry).response.post_id

    def edit_post_on_my_page(self, params, owner_id, filepath):
        photo = self.apivk.save_image(file=MyUtils.file(filepath),
                                      owner_id=owner_id)
        edit_post = self.apivk.wall_edit(params=params)
        assert edit_post.status_code == 200, "Ошибка при отправке запроса"
        return photo

    def create_comment(self, params):
        create_comment = self.apivk.wall_create_comment(params=params)
        assert create_comment.status_code == 200, "Ошибка при отправке запроса"
    
    def check_add_like_this_post(self, params,user_id):
        usersLike = self.apivk.getListLike(params)
        assert usersLike.status_code == 200, "Ошибка при отправке запроса"
        items = JsonConverter.json_converter(usersLike)
        Logger.info(f'Items {items}')
        for i in items.response.items:
            if user_id == str(i):
                return True
            else: return False

    def delete_entry(self, params):
         self.apivk.wall_delete(params=params)