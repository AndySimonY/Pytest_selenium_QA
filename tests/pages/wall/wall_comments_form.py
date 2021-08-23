from selenium.webdriver.common.by import By

"""Элементы"""
from framework.pages.base_page import BasePage
from framework.elements.label import Label
from framework.elements.link import Link


class WallComments(BasePage):

    post_field = ".//div[@id='post_field']"

    show_next_comment = Link(search_condition=By.XPATH,
                           locator=".//div[@class='post_content']//a[contains(@class, 'replies_next_main')]", 
                           name='show next comment')
    

    wall_post_comment_text = Label(search_condition=By.XPATH,
                           locator=".//div[contains(@class, '_reply_content _post_content')]//div[@class='wall_reply_text']", 
                           name='My new comment')
    wall_post_comment_authot = Label(search_condition=By.XPATH,
                           locator=".//div[contains(@class, '_reply_content _post_content')]//a[@class='author']", 
                           name='Post comment author')
    def __init__(self):
        super().__init__(search_condition=By.XPATH, 
                    locator=WallComments.post_field,
                    page_name=self.__class__.__name__)
        super().wait_for_page_opened()

    def check_comment_visiple_right(self, text, autor_name):
        if self.show_next_comment:
            self.show_next_comment.click()
        if self.wall_post_comment_text.get_text() == text and\
           self.wall_post_comment_authot.get_text() == autor_name:
           return True
        else: return False