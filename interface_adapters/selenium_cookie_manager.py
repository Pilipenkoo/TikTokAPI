# interface_adapters/selenium_cookie_manager.py

import os
import pickle
from interfaces.cookie_manager_interface import CookieManagerInterface

class SeleniumCookieManager(CookieManagerInterface):
    def __init__(self, cookies_file='tiktok_cookies.pkl'):
        self.cookies_file = cookies_file

    def load_cookies(self, web_interface):
        if os.path.exists(self.cookies_file) and os.path.getsize(self.cookies_file) > 0:
            try:
                with open(self.cookies_file, 'rb') as file:
                    cookies = pickle.load(file)
                    web_interface.add_cookies(cookies)
            except (EOFError, pickle.UnpicklingError):
                print("Файл с куки поврежден. Пропускаем загрузку куки.")
        else:
            print("Файл с куки не найден или пуст, требуется новая авторизация.")

    def save_cookies(self, cookies):
        with open(self.cookies_file, 'wb') as file:
            pickle.dump(cookies, file)
