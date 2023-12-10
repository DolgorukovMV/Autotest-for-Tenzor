from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

# Настройка логгера
logger = logging.getLogger(__name__)


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.base_url = "https://sbis.ru/"

    def open_url(self, url):
        self.driver.get(url)

    def wait_for_page_load(self, timeout=5):
        """
        Ждет, пока страница полностью загрузится.
        """
        current_url = self.driver.current_url
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.current_url != current_url and self.is_jquery_inactive(d)
        )

    def is_jquery_inactive(self, driver):
        """
        Проверяет, неактивен ли jQuery на странице.
        """
        try:
            return driver.execute_script("return typeof jQuery === 'undefined' || jQuery.active === 0")
        except Exception as ex:
            logger.error(f"Exception in is_jquery_inactive: {ex}")
            return True  # Обработка исключений, если что-то пошло не так

    def find_element(self, by, value):
        return self.driver.find_element(by, value)

    def wait_for_element(self, by, value, timeout=30):
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
        except Exception as ex:
            logger.error(f"Exception in wait_for_element: {ex}")
            raise  # Повторно поднимаем исключение