from selenium.webdriver.common.by import By

"""Элементы"""
from framework.pages.base_page import BasePage
from framework.elements.label import Label
from framework.elements.link import Link

class WallPosts(BasePage):

    unik_wall_el = ".//div[@class='profile_rate_warning']"
    wall_post_text = Label(search_condition=By.XPATH,
                           locator=".//div[@class='post_content']//div[contains(@class, 'wall_post_text')]", 
                           name='My new Post text')
    wall_post_author = Link(search_condition=By.XPATH,
                           locator=".//a[@class='author']", 
                           name='My new Post author')
    wall_photo_id = Link(search_condition=By.XPATH,
                           locator=".//div[@class='post_header_info']//a[contains(@class, 'author')]", 
                           name='Wall photo')

    def __init__(self):
        super().__init__(search_condition=By.XPATH, 
                    locator=WallPosts.unik_wall_el,
                    page_name=self.__class__.__name__)
        super().wait_for_page_opened()

    def check_post_is_visiple_right(self, text, autor_name):
        self.wall_post_text.wait_for_is_present()
        if self.wall_post_text.get_text() == text and\
           self.wall_post_author.get_text() == autor_name:
           return True
        else: return False

    def check_post_changes_and_added_img(self, text, photo_id):
        if self.wall_photo_id and\
           self.wall_photo_id.get_attribute('href') == photo_id and\
           self.wall_post_text == text:
           return True
        else: return False

    def check_post_is_deleted(self):
        return self.wall_post_text.is_displayed