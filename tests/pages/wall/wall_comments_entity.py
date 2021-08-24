from selenium.webdriver.common.by import By

"""Элементы"""
from framework.elements.label import Label
from framework.elements.link import Link

from pages.wall.wall_like_entity import LikeForm

class CommentForm(object):
        
    show_next_comment = Link(search_condition=By.XPATH,
                           locator="//div[@class='post_content']//a[contains(@class, 'replies_next_main')]", 
                           name='show next comment')
    def __init__(self,user_id,post_id, comment_id):
        self.post_id = post_id
        self.user_id = user_id
        self.comment_id = comment_id
        self.wall_post_comment_text = Label(search_condition=By.XPATH,
                            locator=f"//div[@id='post{self.user_id}_{self.post_id}']//div[@id='post{self.user_id}_{self.comment_id}']//div[@class='wall_reply_text']", 
                            name='My new comment')
        self.wall_post_comment_authot = Label(search_condition=By.XPATH,
                            locator=f"//div[@id='post{self.user_id}_{self.post_id}']//div[@id='post{self.user_id}_{self.comment_id}']//div[@class='reply_content']//a[@class='author']", 
                            name='Post comment author')
        self.like_btn = LikeForm(user_id=user_id, post_id=post_id, comment_id=comment_id)
        
    def check_comment_visible_right(self, text, autor_name):
        if self.show_next_comment:
            self.show_next_comment.click()
        if self.wall_post_comment_text.get_text() == text and\
           self.wall_post_comment_authot.get_text() == autor_name:
           return True
        else: return False