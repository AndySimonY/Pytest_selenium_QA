from framework.api.base_api import BaseApi
from tests.config.test_data.urls import Urls
from tests.config.test_data.t_data import Tdata
from framework.utils.logger import Logger

class VKApiUtils(BaseApi):

    def __init__(self, headers, access_tocken):
        self.access_tocken = access_tocken
        super().__init__(headers)

    def wall_post(self, params=[]):
        Logger.info('Создание поста')
        request = self.post(url=self.generate_request_vkapi(
                                 'wall.post', params=params))
        return request

    def wall_edit(self, params=[]):
        Logger.info('Редактирование поста')
        request = self.post(url=self.generate_request_vkapi(
                                 'wall.edit', params=params))
        return request
    
    def wall_create_comment(self, params=[]):
        Logger.info('Создание комента')
        request = self.post(url=self.generate_request_vkapi(
                                 'wall.createComment', params=params))

        return request
    
    def wall_delete(self, params=[]):
        Logger.info('Удаление поста')
        request = self.post(url=self.generate_request_vkapi(
                                 'wall.delete', params=params))
        return request

    def getWallUploadServer(self, group_id):
        request = self.get(url=self.generate_request_vkapi(
                            'photos.getWallUploadServer', 
                             params=f'group_id={group_id}'))
        return request

    def getListLike(self, params):
        Logger.info('Получение списка лайкнувших или что то еще')
        request = self.get(url=self.generate_request_vkapi(
                            'likes.getList', 
                             params=params))
        return request

    def saveWallPhoto(self, params=[]):
        request = self.post(url=self.generate_request_vkapi(
            'photos.saveWallPhoto', params=params
        ))
        a = request.json()
        return request

    def generate_request_vkapi(self, method, version = Tdata.VERSION,
                               params=None, url = Urls.BASE_URL_API):     
        token = self.access_tocken
        part_1 = url + method + '?'
        part_2 = token + '&' + version   
        if isinstance(params, list):
            if len(params) > 1:
                params_query = ''
                for p in params:
                    params_query += p + '&'
                return part_1 + params_query + part_2
            elif len(params) == 1:
                return part_1 + params[0] + '&' + part_2
            else: return part_1 + part_2
        else: 
            if params: 
                return part_1 + params + '&' + part_2
            else: return part_1 + part_2

    def save_image(self, file, owner_id):
        upload_url = self.getWallUploadServer(group_id=owner_id)\
                     .json()['response']['upload_url']
        uploading_img = self.post(upload_url, files=file) #использовать фреймворк
        uploading_img = uploading_img.json()
        photo = uploading_img["photo"]
        server = uploading_img['server']
        hash = uploading_img['hash']
        save_wall_photo = self.saveWallPhoto(params=[f'user_id={owner_id}', 
                            f'photo={photo}', f'server={server}', f'hash={hash}'])
        save_wall_photo = save_wall_photo.json()
        save_photo = "photo" + str(save_wall_photo['response'][0]['owner_id']) +'_'+ str(save_wall_photo['response'][0]['id'])
        return save_photo