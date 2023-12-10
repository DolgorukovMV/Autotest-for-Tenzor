from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
import logging

# Настройка логгера
logger = logging.getLogger(__name__)

class ContactsPage(BasePage):
    def go_to_contacts(self):
        try:
            self.open_url(self.base_url)
            contacts_link = self.wait_for_element(By.LINK_TEXT, "Контакты")
            contacts_link.click()
        except Exception as ex:
            logger.error(f"Exception in go_to_contacts: {ex}")
            raise  # Повторно поднимаем исключение