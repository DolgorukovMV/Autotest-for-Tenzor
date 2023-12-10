from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import logging
# Инициализация логгера
logger = logging.getLogger(__name__)

# Класс BasePage для общих функциональностей
class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.base_url = "https://sbis.ru/"
        print("Logger initialized successfully in BasePage")
# Открыть указанный URL
    def open_url(self, url):
        self.driver.get(url)
# Найти элемент, используя указанные стратегию и значение
    def find_element(self, by, value):
        return self.driver.find_element(by, value)
# Ожидать появления элемента с указанным таймаутом
    def wait_for_element(self, by, value, timeout=30):
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
        except Exception as ex:                    # Залогировать ошибку при возникновении исключения и повторно вызвать исключение
            self.log_error("Exception in wait_for_element", ex)
            raise
 # Ожидать загрузки страницы "О нас"
    def wait_for_about_us_page(self):
        self.wait_for_url_contains("https://tensor.ru/about", "Exception in wait_for_about_us_page")
# Ожидать, что URL содержит указанную строку
    def wait_for_url_contains(self, url, error_message):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.url_contains(url)
            )
        except Exception as ex:
            self.log_error(error_message, ex)
            raise
# Залогировать ошибку
    def log_error(self, message, exception):
        logger.error(f"{message}: {exception}")
        raise
