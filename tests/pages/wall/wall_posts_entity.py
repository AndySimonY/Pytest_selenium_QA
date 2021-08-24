from tests.config.test_data.urls import Urls
from tests.MyUtils.other_utils import MyUtils
from framework.browser.browser import Browser
from selenium.webdriver.common.by import By

"""Элементы"""
from framework.pages.base_page import BasePage
from framework.elements.label import Label
from framework.elements.link import Link

from tests.pages.wall.wall_comments_entity import CommentForm
from tests.pages.wall.wall_like_entity import LikeForm

class PostsForm(BasePage):

    unik_wall_el = "//div[@class='profile_rate_warning']"

    image_src = Link(search_condition=By.XPATH,
                        locator= "//div[@id='pv_photo']//img", 
                        name='image src')

    img_concret = Link(search_condition=By.XPATH,
                        locator= "//img", 
                        name='image')

    def __init__(self, user_id, post_id, photo_id, comments_id):
        if comments_id:
            self.comment = CommentForm(user_id=user_id, post_id=post_id, comments_id=comments_id)

        self.like_btn = LikeForm(user_id=user_id, post_id=post_id, comments_id=comments_id)


        if photo_id:
            self.wall_photo = Link(search_condition=By.XPATH,
                            locator=f"//div[@id='post{user_id}_{post_id}']//a[@href='/photo{user_id}_{photo_id}']", 
                            name='Wall photo')
        self.wall_post_text = Label(search_condition=By.XPATH,
                           locator=f"//div[@id='post{user_id}_{post_id}']//div[@class='post_content']//div[contains(@class, 'wall_post_text')]", 
                           name='My new Post text')
        self.wall_post_author = Link(search_condition=By.XPATH,
                           locator=f"//div[@id='post{user_id}_{post_id}']//a[@class='author']", 
                           name='My new Post author')



    def check_post_is_visiple_right(self, text, autor_name):
        self.wall_post_text.wait_for_is_present()
        if self.wall_post_text.get_text() == text and\
           self.wall_post_author.get_text() == autor_name:
           return True
        else: return False

    def check_post_changes_and_added_img(self, text):
        self.wall_photo.click()
        img_src = self.image_src.get_attribute('src')
        Browser().get_browser().set_url(img_src)
        Browser().get_driver().save_screenshot('screen.png')
        result = MyUtils.get_comparison_result(
                        Urls.LEOPARD_IMAGE_PATH,
                        '/screen.png')
        
        if self.wall_photo and\
            result == 22 and \
            self.wall_post_text == text: #22 - это заранее рассчитанная раздница у фото, 
                                         # если в результате 22 то фото одинаковые 
            return True
        else: return False
    def check_post_is_deleted(self):
        return self.wall_post_text.is_displayed