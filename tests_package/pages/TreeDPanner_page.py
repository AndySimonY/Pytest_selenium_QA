from selenium.webdriver.common.by import By

from framework.pages.base_page import BasePage

from framework.elements.label import Label
from framework.elements.link import Link

from pages.locators.for_treeDPanner_page import Locators
from tests_package.pages.forms.sidebar_buttons_form import SidebarButtonsForm


class TreeDPannerPage(BasePage):
     
    unique_elem = Locators.UNIQUE_ELEMENT

    dialog_window_close = Link(search_condition=By.XPATH,
                               locator=Locators.DIALOG_WINDOW_CLOSE,
                               name='Dialog window close button')

    render_window = Label(search_condition=By.XPATH,
                               locator=unique_elem,
                               name='Render Wondow')

    def __init__(self):
        self.unique_element = TreeDPannerPage.unique_elem
        self.sidebar_buttons_item = SidebarButtonsForm
        super().__init__(search_condition=By.XPATH, 
                    locator=self.unique_element,
                    page_name=self.__class__.__name__)

    
    def close_dialog_window(self):
        self.dialog_window_close.click()

    def dialog_window_is_visible(self):
        return self.dialog_window_close.is_displayed()

    