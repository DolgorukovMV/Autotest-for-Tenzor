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

# Фикстура для инициализации WebDriver
@pytest.fixture
def browser():

    # Создать экземпляр WebDriver с использованием ChromeDriver
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

# Основной тестовый сценарий
def test(browser):
    try:
        # Инициализация базовой страницы
        base_page = BasePage(browser)
        base_page.open_url("https://sbis.ru/")

        # Нахождение элементов с помощью CSS-селектора
        elements = browser.find_elements(By.CSS_SELECTOR, '[href="/download?tab=ereport&innerTab=ereport25"]')
        element = elements[0] if elements else None
        # Если элемент найден, кликнуть на него с использованием JavaScript
        if element:
            logger.info("Clicking on the element using JavaScript...")
            browser.execute_script("arguments[0].click();", element)
        # Инициализация страницы SbisPage
        sbis_page = SbisPage(browser)
        sbis_page.click_sbis_plugin_tab()
        # Проверка текущего URL после клика
        assert "https://sbis.ru/download?tab=plugin&innerTab=default" in browser.current_url
    except Exception as e:
        # Логирование ошибки и повторное поднятие исключения
        logger.exception(f"An error occurred: {e}")
        raise
    finally:
        # Логирование завершения теста
        logger.info("Test completed.")
