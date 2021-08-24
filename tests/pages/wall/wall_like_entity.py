from selenium.webdriver.common.by import By

"""Элементы"""
from framework.pages.base_page import BasePage
from framework.elements.button import Button

class LikeForm:

    def __init__(self, user_id, post_id, comment_id):
        
        self.add_like_post_btn = Button(search_condition=By.XPATH,
                           locator=f"//div[@id='post{user_id}_{post_id}']//div[contains(@class,'like_btns')]/a", 
                           name='Like btn for post')
        if comment_id:
            self.add_like_comment_btn = Button(search_condition=By.XPATH,
                            locator=f"//div[@id='post{user_id}_{post_id}']//div[@id='post{user_id}_{comment_id}']//div[contains(@class,'like_btns')]/a", 
                            name='Like btn for comment')

    def add_like_post(self):
        self.add_like_post_btn.click()

    