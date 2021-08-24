from enum import Enum

class VkApiMethod(Enum):

    get_users = 'users.get'
    get_wall_upload_server = 'photos.getWallUploadServer'
    get_list = 'likes.getList'

    wall_post = 'wall.post'
    wall_edit = 'wall.edit'
    wall_create_comment = 'wall.createComment'
    wall_delete = 'wall.delete'
    save_wall_photo = 'photos.saveWallPhoto'

