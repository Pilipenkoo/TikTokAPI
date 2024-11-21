# interface_adapters/selenium_web_interface.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from interfaces.web_interface import WebInterface

class SeleniumWebInterface(WebInterface):
    def __init__(self, driver):
        self.driver = driver

    def navigate_to(self, url):
        self.driver.get(url)

    def find_element(self, locator):
        by = self._get_by(locator['by'])
        return self.driver.find_element(by, locator['value'])

    def find_elements(self, locator):
        by = self._get_by(locator['by'])
        return self.driver.find_elements(by, locator['value'])

    def click_element(self, element):
        element.click()

    def get_page_source(self):
        return self.driver.page_source

    def execute_script(self, script, element):
        return self.driver.execute_script(script, element)

    def get_cookies(self):
        return self.driver.get_cookies()

    def add_cookies(self, cookies):
        for cookie in cookies:
            self.driver.add_cookie(cookie)

    def refresh(self):
        self.driver.refresh()

    def wait_until_clickable(self, locator, timeout):
        by = self._get_by(locator['by'])
        element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((by, locator['value']))
        )
        return element

    def wait_until_present(self, locator, timeout):
        by = self._get_by(locator['by'])
        element = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, locator['value']))
        )
        return element

    def _get_by(self, by_str):
        mapping = {
            'id': By.ID,
            'xpath': By.XPATH,
            'name': By.NAME,
            'css_selector': By.CSS_SELECTOR,
            'class_name': By.CLASS_NAME,
            'tag_name': By.TAG_NAME,
            'link_text': By.LINK_TEXT,
            'partial_link_text': By.PARTIAL_LINK_TEXT
        }
        return mapping.get(by_str.lower())
