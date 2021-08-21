from requests.api import request
from framework.api.base_api import BaseApi
from tests.config.test_data.urls import Urls
from tests.config.test_data.t_data import Tdata

class VKApiUtils(BaseApi):

    def __init__(self, headers, access_tocken):
        self.access_tocken = access_tocken
        super().__init__(headers)

    def wall_post(self, params=[]):
        request = self.post(url=self.generate_request_vkapi(
                                 'wall.post', params=params))
        return request

    def wall_edit(self, params=[]):
        request = self.post(url=self.generate_request_vkapi(
                                 'wall.edit', params=params))
        return request

    def getWallUploadServer(self, group_id):
        request = self.get(url=self.generate_request_vkapi(
                            'photos.getWallUploadServer', 
                             params=f'group_id={group_id}'))
        return request

    def saveWallPhoto(self, user_id, photo, server, hash):
        request = self.post(url=self.generate_request_vkapi(
            'photos.saveWallPhoto', params=f'user_id={user_id}'
        ), )

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
                return part_1 + params + part_2
            else: return part_1 + part_2