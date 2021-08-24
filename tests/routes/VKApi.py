from framework.utils.logger import Logger
from framework.api.json_converter import JsonConverter

from tests.routes.VKApiUtils import VKApiUtils

from tests.config.test_data.status_code import StatusCode

from tests.other_utils import MyUtils

class VKApi:

    def __init__(self, headers, access_tocken):
        self.apivk = VKApiUtils(headers, 
                                access_tocken)

    def get_current_user(self):
        user = self.apivk.get_user()
        assert user.status_code == StatusCode.status_200, (
               "Ошибка при отправке запроса")
        return JsonConverter.json_converter(user).response[0].id

    def create_post_on_my_page(self, message):
        create_entry = self.apivk.wall_post(params=f'messae={message}')
        assert create_entry.status_code == StatusCode.status_200, (
               "Ошибка при отправке запроса")
        return JsonConverter.json_converter(create_entry).response.post_id

    def edit_post_on_my_page(self, owner_id, 
                             post_id,message,filepath):
        photo = self.apivk.save_image(file=MyUtils.file(filepath),
                                      owner_id=owner_id)
        edit_post = self.apivk.wall_edit(params=[f'owner_id={owner_id}', 
                                        f'post_id={post_id}', 
                                        f'message={message}'])
        assert edit_post.status_code == StatusCode.status_200, (
              "Ошибка при отправке запроса")
        return photo

    def create_comment(self, owner_id, post_id, message ):
        create_comment = self.apivk.wall_create_comment(params=[
        f'owner_id={owner_id}',f'post_id={post_id}', 
        f'message={message}'])
        assert create_comment.status_code == StatusCode.status_200, (
               "Ошибка при отправке запроса")
        return JsonConverter.json_converter(create_comment).response.comment_id
    
    def check_add_like_this_post(self, owner_id, post_id):
        usersLike = self.apivk.getListLike(params=['type=post', 
                                           f'owner_id={owner_id}', 
                                           f'item_id={post_id}',
                                           'filter=likes'])
        assert usersLike.status_code == StatusCode.status_200,(
               "Ошибка при отправке запроса")
        items = JsonConverter.json_converter(usersLike)
        Logger.info(f'Items {items}')
        for i in items.response.items:
            if owner_id == str(i):
                return True
            else: return False

    def delete_entry(self, owner_id, post_id):
         self.apivk.wall_delete(params=[f'owner_id={owner_id}', 
                                f'post_id={post_id}'])