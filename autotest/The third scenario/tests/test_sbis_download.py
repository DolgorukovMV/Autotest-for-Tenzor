import pytest

import logging

from selenium import webdriver
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.sbis_page import SbisPage, logger

# Создание логгера
logger.setLevel(logging.DEBUG)

# Создание и настройка обработчика файла
file_handler = logging.FileHandler(r'C:\Users\iriy9\PycharmProjects\Thirdtest\logs\py_log.log')
file_handler.setLevel(logging.DEBUG)

# Создание и настройка обработчика консоли
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Создание и настройка форматтера
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Добавление обработчиков к логгеру
logger.addHandler(file_handler)
logger.addHandler(console_handler)

print(f"Logger configured. Log file: {'C:/test_log.txt'}")
logger.info("Test started")


@pytest.fixture
def browser():

    # Создать экземпляр WebDriver с использованием ChromeDriver
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


def test(browser):
    try:
        base_page = BasePage(browser)
        base_page.open_url("https://sbis.ru/")
        # Максимизация окна браузера
        # browser.maximize_window()
        # Прокрутка страницы вниз
        #  browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        elements = browser.find_elements(By.CSS_SELECTOR, '[href="/download?tab=ereport&innerTab=ereport25"]')
        element = elements[0] if elements else None

        if element:
            logger.info("Clicking on the element using JavaScript...")
            browser.execute_script("arguments[0].click();", element)

        sbis_page = SbisPage(browser)
        sbis_page.click_sbis_plugin_tab()

       # assert "https://sbis.ru/download?tab=plugin&innerTab=default" in browser.current_url
    except Exception as e:
        logger.exception(f"An error occurred: {e}")
        raise
    finally:
        logger.info("Test completed.")