import os

from selenium.common import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import logging

logger = logging.getLogger(__name__)


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.base_url = "https://sbis.ru"

    def open_url(self, url):
        self.driver.get(url)

    def wait_for_page_load(self, timeout=5):
        """Ждет, пока страница полностью загрузится"""
        logger.info(f"Waiting for page load. Current URL: {self.driver.current_url}")

        current_url = self.driver.current_url
        WebDriverWait(self.driver, timeout).until(
            lambda driver: driver.current_url != current_url and self.is_jquery_inactive(driver)
        )

        logger.info(f"Page loaded successfully. New URL: {self.driver.current_url}")

    def is_jquery_inactive(self, driver):
        logger.info("Checking if jQuery is inactive...")

        try:
            # Используйте JavaScript для проверки активности jQuery
            result = driver.execute_script("return jQuery.active == 0")
            logger.info(f"jQuery is {'inactive' if result else 'active'}")
            return result
        except WebDriverException as e:
            # Обработка исключения (если необходимо)
            logger.error(f"An error occurred while checking jQuery activity: {str(e)}")
            return False

    def find_element(self, by, value):
        return self.driver.find_element(by, value)

    def wait_for_element_to_be_clickable(self, by, value, timeout=30):
        try:
            self.wait_for_page_load()  # Ждем полной загрузки страницы
            return WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
        except Exception as ex:
            logger.error(f"Exception in wait_for_element_to_be_clickable: {ex}")
            raise  # Повторно поднимаем исключение

    def execute_js_click(self, element):
        self.driver.execute_script("arguments[0].click();", element)

    def wait_for_element(self, by, value, timeout=10):
        try:
            logger.info(f"Waiting for element by {by} with value {value}")
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
        except Exception as ex:
            logger.error(f"Element not found by {by} with value {value} within {timeout} seconds. Error: {ex}")
            raise

    def wait_for_file_to_download(self, file_path, timeout=60):
        start_time = time.time()

        # Проверить, существует ли файл до начала ожидания
        if os.path.exists(file_path):
            return

        # Используем явное ожидание
        wait = WebDriverWait(self.driver, timeout)
        wait.until(lambda driver: os.path.exists(file_path) or (time.time() - start_time > timeout),
                   message=f"File not downloaded within {timeout} seconds.")