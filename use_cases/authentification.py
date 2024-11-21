# use_cases/authentication_use_case.py

from interfaces.web_interface import WebInterface
from interfaces.cookie_manager_interface import CookieManagerInterface

class AuthenticationUseCase:
    def __init__(self, web_interface: WebInterface, cookie_manager: CookieManagerInterface):
        self.web_interface = web_interface
        self.cookie_manager = cookie_manager

    def is_logged_in(self) -> bool:
        self.web_interface.navigate_to('https://www.tiktok.com/')
        page_source = self.web_interface.get_page_source()
        return "Войти" not in page_source

    def login(self):
        self.web_interface.navigate_to('https://www.tiktok.com/login')
        try:
            locator = {"by": "xpath", "value": "//div[contains(text(), 'Продолжить с Google')]"}
            google_login_button = self.web_interface.wait_until_clickable(locator, timeout=20)
            self.web_interface.click_element(google_login_button)
            input("Пожалуйста, выполните вход вручную и нажмите Enter...")
            cookies = self.web_interface.get_cookies()
            self.cookie_manager.save_cookies(cookies)
        except Exception:
            print("Не удалось найти элемент для входа через Google.")
