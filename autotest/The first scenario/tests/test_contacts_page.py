import pytest
import logging
from selenium import webdriver
from pages.contacts_page import ContactsPage, logger
from datetime import datetime


# Создание логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Создание и настройка обработчика файла
file_handler = logging.FileHandler(r'C:\Users\iriy9\PycharmProjects\firstTest\logs\py_log.log')
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


def test_go_to_contacts_page(browser):
    try:
        contacts_page = ContactsPage(browser)
        contacts_page.go_to_contacts()

        # Проверяем, что мы находимся на странице "Контакты"
        assert "Контакты" in browser.title

        # Вызываем новый метод для поиска и клика по баннеру "Тензор"
        contacts_page.click_tensor_banner()

        # Проверить, что после клика по баннеру "Тензор" произошло ожидаемое изменение
        assert "tensor.ru" in browser.current_url

        # После клика по баннеру "Тензор", ищем блок "Сила в людях"
        block_sila_v_lyudyakh = contacts_page.find_sila_v_lyudyakh_block()
        assert block_sila_v_lyudyakh is not None, "Блок 'Сила в людях' не найден на странице"

        # Перейти в блоке "Сила в людях" в "Подробнее"
        contacts_page.click_more_about_us()

        # Убедитесь, что открыта нужная страница
        contacts_page.wait_for_about_us_page()

        # Проверка размеров фотографий
        try:
            contacts_page.check_photos_dimensions()
        except AssertionError as e:
            # Логируем ошибку вместо вывода в консоль
            logger.error(f"AssertionError in test_go_to_contacts_page: {e}")
            raise  # Повторно поднимаем исключение, чтобы тест был отмечен как проваленный
    except Exception as ex:
        logger.error(f"Exception in test_go_to_contacts_page: {ex}")
        raise  # Повторно поднимаем исключение, чтобы тест был отмечен как проваленный
    finally:
        logger.info("Test completed")