from selenium.webdriver.support.wait import WebDriverWait
from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import logging
# Инициализация логгера
logger = logging.getLogger(__name__)

# Класс ContactsPage, который наследуется от BasePage
class ContactsPage(BasePage):
    # Метод для перехода на страницу "Контакты"
    def go_to_contacts(self):
        try:
            self.open_url(self.base_url)
            # Найти ссылку на "Контакты" и кликнуть
            contacts_link = self.wait_for_element(By.LINK_TEXT, "Контакты")
            contacts_link.click()
        except Exception as ex:
            self.log_error("Exception in go_to_contacts", ex)
# Метод для клика по баннеру "Тензор"
    def click_tensor_banner(self):
        try:
            # Найти изображение баннера "Тензор" и кликнуть
            tensor_banner_img = self.wait_for_element(By.XPATH,
                                                      "//img[contains(@alt, 'Разработчик системы СБИС — компания «Тензор»')]")
            tensor_banner_img.click()
            # Переключиться на новую вкладку и дождаться, что URL содержит "tensor.ru"
            self.switch_to_new_tab()
            self.wait_for_url_contains("tensor.ru", "Exception in click_tensor_banner")
        except Exception as ex:
            self.log_error("Exception in click_tensor_banner", ex)
# Метод для переключения на новую вкладку
    def switch_to_new_tab(self):
        all_handles = self.driver.window_handles
        new_tab_handle = all_handles[-1]
        self.driver.switch_to.window(new_tab_handle)
# Метод для поиска блока "Сила в людях"
    def find_sila_v_lyudyakh_block(self):
        return self.find_element(By.CLASS_NAME, "tensor_ru-Index__block4-content")
# Метод для клика по ссылке "Подробнее о нас"
    def click_more_about_us(self):
        more_about_us_link = self.wait_for_element(By.XPATH,
                                                   "//a[@class='tensor_ru-link tensor_ru-Index__link' and @href='/about'][last()]")
        self.driver.execute_script("arguments[0].click();", more_about_us_link)
# Метод для проверки размеров фотографий в секции работы
    def check_photos_dimensions(self):
        work_section = self.wait_for_element(By.XPATH,
                                             "//div[@class='tensor_ru-container tensor_ru-section tensor_ru-About__block3']")
        photos = work_section.find_elements(By.XPATH,
                                            "//img[@class='tensor_ru-About__block3-image new_lazy loaded']")

        if len(photos) > 1:
            # Получить размеры первой фотографии
            first_photo = photos[0]
            first_height, first_width = first_photo.get_attribute("height"), first_photo.get_attribute("width")
            # Проверить размеры остальных фотографий
            for photo in photos[1:]:
                height, width = photo.get_attribute("height"), photo.get_attribute("width")
                assert height == first_height, f"Высота фотографии не одинакова. Ожидалось {first_height}, фактически {height}"
                assert width == first_width, f"Ширина фотографии не одинакова. Ожидалось {first_width}, фактически {width}"
        else:
            logger.info("Нет фотографий для проверки")
