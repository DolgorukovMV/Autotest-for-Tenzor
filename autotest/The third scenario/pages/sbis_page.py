import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
import logging

# Настройка логгера
logger = logging.getLogger(__name__)


class SbisPage(BasePage):
    def go_to_page(self):
        try:
            self.open_url(self.base_url)
            contacts_link = self.wait_for_element(By.LINK_TEXT, "Скачать СБИС")
            contacts_link.click()
        except Exception as ex:
            logger.error(f"Exception in go_to_contacts: {ex}")
            raise  # Повторно поднимаем исключение

    def click_sbis_plugin_tab(self):
        try:
            # Открываем ссылку
            self.driver.get("https://sbis.ru/download?tab=plugin&innerTab=default")

            # Подождать, пока элемент для скачивания не станет видимым
            download_element = self.wait_for_element(By.XPATH,
                                                     '//a[@href="https://update.sbis.ru/Sbis3Plugin/master/win32/sbisplugin-setup-web.exe" and contains(@class, "sbis_ru-DownloadNew-loadLink__link") and contains(@class, "js-link")]')

            logger.info("Clicking on the download link...")
            download_element.click()

            # Подождать, пока файл скачается
            download_path = "C:/Users/iriy9/Downloads"
            downloaded_file_path = os.path.join(download_path, "sbisplugin-setup-web.exe")
            self.wait_for_file_to_download(downloaded_file_path, timeout=60)  # Увеличьте таймаут, если это необходимо

            # Убедимся, что файл скачался
            assert os.path.exists(downloaded_file_path), "Downloaded file not found."

            # Сравнить размер скачанного файла с ожидаемым размером (6.94 МБ)
            expected_file_size = 6.94   # в байтах
            actual_file_size = os.path.getsize(downloaded_file_path)
            actual_file_size = round(actual_file_size/(1024*1024), 2)
            assert actual_file_size == expected_file_size, f"Downloaded file size mismatch. Expected: {expected_file_size} bytes, Actual: {actual_file_size} bytes."

        except Exception as ex:
            logger.error(f"An error occurred: {ex}")
            raise
