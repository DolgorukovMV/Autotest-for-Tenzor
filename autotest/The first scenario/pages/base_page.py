from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import logging

logger = logging.getLogger(__name__)


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.base_url = "https://sbis.ru/"
        print("Logger initialized successfully in BasePage")

    def open_url(self, url):
        self.driver.get(url)

    def find_element(self, by, value):
        return self.driver.find_element(by, value)

    def wait_for_element(self, by, value, timeout=30):
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
        except Exception as ex:
            self.log_error("Exception in wait_for_element", ex)
            raise

    def wait_for_about_us_page(self):
        self.wait_for_url_contains("https://tensor.ru/about", "Exception in wait_for_about_us_page")

    def wait_for_url_contains(self, url, error_message):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.url_contains(url)
            )
        except Exception as ex:
            self.log_error(error_message, ex)
            raise

    def log_error(self, message, exception):
        logger.error(f"{message}: {exception}")
        raise