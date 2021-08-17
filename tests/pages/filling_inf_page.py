import time
import pyautogui
from framework.pages.base_page import BasePage
from selenium.webdriver.common.by import By
from framework.elements.link import Link
from framework.elements.label import Label
from framework.elements.button import Button
from tests.other_utils import generate_random_number

class FillingInfPage(BasePage):
     
    logo = ".//div[@class='logo__icon']"

    checkbox_interes = Button(search_condition=By.XPATH,
                                  locator=".//div[@class='avatar-and-interests__interests-list__item']//span[@class='checkbox__box']",
                                  name='Checkbox Interes')
    upload_img = Link(search_condition=By.XPATH,
                           locator=".//a[@class='avatar-and-interests__upload-button']",
                           name='Upload Image'
                                )
    button_next_of_user_inf_side = Button(search_condition=By.XPATH,
                                       locator=".//button[contains(@class,'button--stroked')]",
                                       name='Button Next')
    personal_details = Label(search_condition=By.XPATH,
                                 locator=".//div[@class='personal-details__form']",
                                 name='Personal inf. details')

    def __init__(self):
        super().__init__(search_condition=By.XPATH, 
                         locator=FillingInfPage.logo,
                         page_name=self.__class__.__name__)
        super().wait_for_page_opened()

    def get_checkbox_items(self):
        return self.checkbox_interes.get_elements()

    def click_unselect_all(self, index, items):
        items[index].click()
    
    def select_random_interes(self, count, items, elem):
        length = len(items)
        number_of_interes = generate_random_number(count, length, elem)
        for el in range(len(number_of_interes)):
                items[number_of_interes[el]].click()

    def upload_image(self, file_path):
        self.upload_img.click()
        time.sleep(2) #Небольшое ожидание открытия диалогового окна ОС
        pyautogui.write(file_path)
        pyautogui.press('enter')
        time.sleep(1) # Ожидание закрытия окна, далее продолжаем тетирование

    def click_next_button(self):
        self.button_next_of_user_inf_side.wait_for_clickable()
        self.button_next_of_user_inf_side.click()
    
    def is_displaeyd_following_person_inf(self):
        return self.personal_details.is_displayed