# interfaces/cookie_manager_interface.py

from abc import ABC, abstractmethod

class CookieManagerInterface(ABC):
    @abstractmethod
    def load_cookies(self, web_interface):
        pass

    @abstractmethod
    def save_cookies(self, cookies):
        pass
