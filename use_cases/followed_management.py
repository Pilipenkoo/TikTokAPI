# use_cases/follower_management_use_case.py

import time
from entities.follower import Follower
from interfaces.web_interface import WebInterface

class FollowerManagementUseCase:
    def __init__(self, web_interface: WebInterface):
        self.web_interface = web_interface

    def get_followers(self, username: str):
        self.web_interface.navigate_to(f'https://www.tiktok.com/@{username}')
        try:
            locator = {"by": "xpath", "value": "//span[@data-e2e='followers']"}
            followers_button = self.web_interface.wait_until_clickable(locator, timeout=20)
            self.web_interface.click_element(followers_button)

            # Ожидаем загрузки списка подписчиков
            locator_list = {"by": "xpath", "value": "//div[@data-e2e='user-list']"}
            self.web_interface.wait_until_present(locator_list, timeout=20)

            # Прокручиваем список подписчиков
            scrollable_div = self.web_interface.find_element(locator_list)
            last_height = self.web_interface.execute_script("return arguments[0].scrollHeight", scrollable_div)

            while True:
                self.web_interface.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
                time.sleep(1)
                new_height = self.web_interface.execute_script("return arguments[0].scrollHeight", scrollable_div)
                if new_height == last_height:
                    break
                last_height = new_height

            # Собираем ссылки на профили подписчиков
            locator_followers = {
                "by": "xpath",
                "value": "//div[@data-e2e='user-item']//a[@data-e2e='user-card-avatar']"
            }
            followers_elements = self.web_interface.find_elements(locator_followers)
            followers = set()
            for elem in followers_elements:
                profile_url = elem.get_attribute("href")
                username = profile_url.split('@')[-1]
                followers.add(Follower(username, profile_url))
            return followers

        except Exception:
            print("Не удалось загрузить список подписчиков.")
            return set()
