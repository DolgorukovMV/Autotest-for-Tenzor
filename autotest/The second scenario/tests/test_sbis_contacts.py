import pytest
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.contacts_page import ContactsPage, logger

# Создание логгера
logger.setLevel(logging.DEBUG)

# Создание и настройка обработчика файла
file_handler = logging.FileHandler(r'C:\Users\iriy9\PycharmProjects\second scenario\logs\py_log.log')
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
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test(browser):
    try:
        base_page = BasePage(browser)
        base_page.open_url("https://sbis.ru/")
        base_page.wait_for_element(By.LINK_TEXT, "Контакты").click()

        # Проверяем, что мы находимся на странице "Контакты"
        assert "Контакты" in browser.title

        contacts_page = ContactsPage(browser)
        # Добавляем проверку региона (в данном случае, Нижегородская обл.)
        region_element = contacts_page.wait_for_element(By.XPATH,
                                                        "//span[@class='sbis_ru-Region-Chooser__text sbis_ru-link']")
        assert "Нижегородская обл." in region_element.text

        # Добавляем проверку наличия списка партнеров
        partners_list = contacts_page.wait_for_element(By.CLASS_NAME,
                                                       "sbisru-Contacts-List__col.ws-flex-shrink-1.ws-flex-grow-1")
        assert partners_list.is_displayed()

        # Кликаем на элемент с текстом "Нижегородская обл." для открытия панели выбора региона
        region_chooser = base_page.wait_for_element(By.XPATH,
                                                    "//span[contains(@class, 'sbis_ru-Region-Chooser__text') and contains(text(), 'Нижегородская обл.')]")
        region_chooser.click()

        # Ждем появления панели выбора региона
        region_panel = base_page.wait_for_element(By.CLASS_NAME, 'sbis_ru-Region-Panel')

        # Находим элемент с текстом "Камчатский край" и кликаем на него
        kamchatka_region = region_panel.find_element(By.XPATH,
                                                     "//span[contains(@class, 'sbis_ru-link') and contains(text(), 'Камчатский край')]")
        kamchatka_region.click()

        # Ждем, чтобы страница обновилась после выбора региона
        base_page.wait_for_page_load()

        # Проверяем, что выбранный регион подставился
        selected_region = region_chooser.text
        assert selected_region == "Камчатский край"

        # Проверяем, что список партнеров изменился (можете использовать соответствующий селектор для списка)
        partners_list = contacts_page.wait_for_element(By.XPATH,
                                                       "//div[@class='sbisru-Contacts-List__col ws-flex-shrink-1 ws-flex-grow-1']")
        assert partners_list.is_displayed()

        # Проверяем, что URL и title содержат информацию выбранного региона
        assert "СБИС Контакты — Камчатский край" in browser.title
        assert "41-kamchatskij-kraj?tab=clients" in browser.current_url
        # Добавьте шаги для изменения региона и проверки информации

    except Exception as ex:
        logger.error(f"Exception in test_change_region_and_check_info: {ex}")
        raise  # Повторно поднимаем исключение, чтобы тест был отмечен как проваленный
    finally:
        logger.info("Test completed")