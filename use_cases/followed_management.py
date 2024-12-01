# use_cases/follower_management_use_case.py
import json
import time
from entities.follower import Follower
from interfaces.web_interface import WebInterface

class FollowerManagementUseCase:
    def __init__(self, web_interface: WebInterface):
        self.web_interface = web_interface

    def get_followers(self, username):
        self.web_interface.navigate_to(f'https://www.tiktok.com/@{username}')
        try:
            # Нажимаем на кнопку "Подписчики"
            locator_button = {"by": "xpath", "value": "//span[@data-e2e='followers']"}
            followers_button = self.web_interface.wait_until_clickable(locator_button, timeout=30)
            self.web_interface.click_element(followers_button)

            # Ожидаем загрузки списка подписчиков
            locator_list = {
                "by": "xpath",
                "value": "//div[contains(@class, 'DivUserListContainer')]"
            }
            scrollable_div = self.web_interface.wait_until_present(locator_list, timeout=30)

            # Прокручиваем список и собираем подписчиков
            followers_set = set()
            last_count = 0
            max_attempts = 1
            attempts = 0

            while True:
                # Прокручиваем вниз
                self.web_interface.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
                time.sleep(2)  # Ждем загрузки новых элементов

                # Нажимаем на кнопки "Добавить в ответ"
                add_buttons = self.web_interface.find_elements({
                    "by": "xpath",
                    "value": "//button[contains(@aria-label, 'Добавить в ответ') and @data-e2e='follow-button']"
                })

                for button in add_buttons:
                    try:
                        self.web_interface.click_element(button)
                        time.sleep(1)  # Небольшая пауза между нажатиями
                    except Exception as e:
                        print(f"Не удалось нажать на кнопку 'Добавить в ответ': {e}")

                # Собираем элементы подписчиков
                followers_elements = self.web_interface.find_elements({
                    "by": "xpath",
                    "value": "//li//a[contains(@class, 'StyledLink-StyledUserInfoLink')]"
                })
                current_count = len(followers_elements)

                # Проверяем, достигли ли конца списка
                if current_count == last_count:
                    attempts += 1
                    if attempts >= max_attempts:
                        break
                else:
                    attempts = 0
                    last_count = current_count

                # Собираем данные о подписчиках
                for elem in followers_elements:
                    href = elem.get_attribute("href")
                    if href.startswith('https://www.tiktok.com'):
                        profile_url = href
                        username = href.split('@')[-1]
                        followers_set.add(Follower(username, profile_url))

            return followers_set

        except Exception as e:
            print(f"Не удалось загрузить список подписчиков: {e}")
            import traceback
            traceback.print_exc()
            return set()
