# interfaces/web_interface.py

from abc import ABC, abstractmethod

class WebInterface(ABC):
    @abstractmethod
    def navigate_to(self, url: str):
        pass

    @abstractmethod
    def find_element(self, locator: dict):
        pass

    @abstractmethod
    def wait_until_clickable(self, locator: dict, timeout: int):
        pass

    @abstractmethod
    def click_element(self, element):
        pass

    @abstractmethod
    def get_page_source(self) -> str:
        pass

    @abstractmethod
    def get_cookies(self):
        pass

    @abstractmethod
    def add_cookies(self, cookies):
        pass

    @abstractmethod
    def refresh(self):
        pass

    @abstractmethod
    def execute_script(self, script: str, element):
        pass

    @abstractmethod
    def find_elements(self, locator: dict):
        pass
