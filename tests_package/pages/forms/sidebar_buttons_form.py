from selenium.webdriver.common.by import By
from framework.elements.button import Button
from framework.elements.label import Label
from tests_package.pages.forms.locators.for_sidebar_buttons_form import Locators

class SidebarButtonsForm:
      
      """Main Menu"""
      furnish_your_room = Locators.FURNISH_YOU_ROOM

      """Sub Menu"""
      sub_menu_during_room = Locators.DINING_ROOM
      sub_menu_during_room_elements = Locators.DINING_ROOM_ELEMENTS

      @staticmethod
      def navigate(locator=''):
            item = Button(search_condition=By.XPATH,
                               locator=locator,
                               name=f'Sidebar item locator -- {locator}')
            item.wait_for_clickable()
            item.click()

      @staticmethod
      def menu_is_displayed(sub_menu):
            items = Label(search_condition=By.XPATH,
                                locator=sub_menu,
                                name=f'During room elements')
            return items.is_displayed()

      @staticmethod
      def get_menu_items(sub_menu, is_list=False):
            if is_list:
                  items = Label(search_condition=By.XPATH,
                                locator=sub_menu,
                                name=f'During room elements')
                  return items.get_elements()
            else:
                  items = Label(search_condition=By.XPATH,
                                locator=sub_menu,
                                name=f'During room elements')
                  return items
                