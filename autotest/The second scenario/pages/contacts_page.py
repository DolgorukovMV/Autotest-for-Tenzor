from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
import logging

# Настройка логгера
logger = logging.getLogger(__name__)
# Класс ContactsPage, наследующийся от BasePage
class ContactsPage(BasePage):
    # Метод для перехода на страницу "Контакты"
    def go_to_contacts(self):
        try:
            # Открываем указанный URL
            self.open_url(self.base_url)
            # Находим ссылку "Контакты" и кликаем
            contacts_link = self.wait_for_element(By.LINK_TEXT, "Контакты")
            contacts_link.click()
        except Exception as ex:
            # Логируем ошибку и повторно поднимаем исключение
            logger.error(f"Exception in go_to_contacts: {ex}")
            raise  # Повторно поднимаем исключение
