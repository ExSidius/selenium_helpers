import datetime
import random
import time

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def click(driver, element):
    driver.execute_script("arguments[0].click();", element)


class YouFindPlaceHolder:
    def __init__(self, text):
        self.text = text

    def __call__(self, driver):
        element = driver.find_element_by_xpath(f'//input[@placeholder="{self.text}"]')
        if element:
            return element
        else:
            return False


class YouFindText:
    def __init__(self, text):
        self.text = text

    def __call__(self, driver):
        element = driver.find_element_by_xpath(f'//*[contains(text(), "{self.text}")]')
        if element:
            return element
        else:
            return False


class YouFindButtonText:
    def __init__(self, text):
        self.text = text

    def __call__(self, driver):
        element = driver.find_element_by_xpath(f'//button[.="{self.text}"]')
        if element:
            return element
        else:
            return False


class YouFindAllText:
    def __init__(self, text):
        self.text = text

    def __call__(self, driver):
        elements = driver.find_elements_by_xpath(f'//*[contains(text(), "{self.text}")]')
        if elements:
            return elements
        else:
            return False


class URLToBe:
    def __init__(self, url):
        self.url = url

    def __call__(self, driver):
        try:
            res = EC.url_to_be(self.url)(driver)
            if res:
                return res
        except:  # pylint: disable=bare-except
            pass
        return EC.url_to_be(f'{self.url}/')(driver)


def wait_until(driver, expected_condition, value, timeout=10):
    conveniences = {
        'title is': EC.title_is,
        'title contains': EC.title_contains,
        'url matches': EC.url_matches,
        'url is': URLToBe,
        'url contains': EC.url_contains,
        'you find': EC.presence_of_element_located,
        'you find all': EC.presence_of_all_elements_located,
        'you find text': YouFindText,
        'you find button text': YouFindButtonText,
        'you find all text': YouFindAllText,
        'you find placeholder': YouFindPlaceHolder,
        "you don't find": EC.staleness_of,
    }
    ec = conveniences[expected_condition]
    msg = f'{expected_condition} {value}'
    return WebDriverWait(driver, timeout).until(ec(value), message=msg)


def fill_searchable_select(driver, element, content):
    el = wait_until(driver, 'you find', element)
    click(driver, el)
    el.clear()
    el.send_keys(content)
    while True:
        select_items = wait_until(driver, 'you find all', (By.CLASS_NAME, 'el-select-dropdown__item'))
        try:
            if len([item for item in select_items if item.text == content]) == 1:
                break
        except StaleElementReferenceException:
            pass
    el.send_keys(Keys.ENTER)


def potential_refresh(driver, expected_condition, value, chance=0.99):
    if random.uniform(0, 1) > chance:
        driver.refresh()
    return wait_until(driver, expected_condition, value)


def timeout(duration, exception):
    def decorator(f):
        def wrapper(*args, **kwargs):
            start = datetime.datetime.now()
            while True:
                if f(*args, **kwargs):
                    break

                if (datetime.datetime.now() - start).seconds // 60 > duration:
                    raise Exception(exception)

        return wrapper

    return decorator