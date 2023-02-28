import configparser
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


def get_auth_data(data):
    config = configparser.ConfigParser()
    config.read("settings.ini")
    return config['auth'][data]


def wait_element(driver, delay_seconds=1, by=By.TAG_NAME, value=None):
    return WebDriverWait(driver, delay_seconds).until(
        expected_conditions.presence_of_element_located((by, value))
    )


class TestYandexAuth(unittest.TestCase):
    def test_auth(self):
        driver = webdriver.Chrome()

        url = 'https://passport.yandex.ru/auth/'
        driver.get(url=url)

        input_email = driver.find_element(By.ID, 'passp-field-login')
        input_email.send_keys(get_auth_data('login'))
        login_button = driver.find_element(By.ID, 'passp:sign-in')
        login_button.click()

        wait_element(driver, 3, By.ID, 'passp-field-passwd')

        input_password = driver.find_element(By.ID, 'passp-field-passwd')
        input_password.send_keys(get_auth_data('password'))
        login_button = driver.find_element(By.ID, 'passp:sign-in')
        login_button.click()

        wait_element(driver, 20, By.XPATH, '//div[@class="UserID-Avatar "]')

        user_icon = driver.find_element(By.XPATH, '//div[@class="UserID-Avatar "]')
        user_icon.click()


if __name__ == '__main__':
    unittest.main()
