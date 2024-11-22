# frameworks_and_drivers/main.py

from selenium.common.exceptions import WebDriverException
from interface_adapters.selenium_driver import setup_driver
from interface_adapters.selenium_web_interface import SeleniumWebInterface
from interface_adapters.selenium_cookie_manager import SeleniumCookieManager
from use_cases.authentification import AuthenticationUseCase
from use_cases.followed_management import FollowerManagementUseCase
from use_cases.message_sending import MessageSendingUseCase
from framework_driver.follower_file_manager import save_followers_to_file, load_followers_from_file

import time

def main():
    driver = setup_driver()
    web_interface = SeleniumWebInterface(driver)
    cookie_manager = SeleniumCookieManager()
    auth_use_case = AuthenticationUseCase(web_interface, cookie_manager)
    follower_management_use_case = FollowerManagementUseCase(web_interface)
    message_sending_use_case = MessageSendingUseCase(web_interface)

    try:
        web_interface.navigate_to('https://www.tiktok.com/')
        cookie_manager.load_cookies(web_interface)
        web_interface.refresh()

        if not auth_use_case.is_logged_in():
            auth_use_case.login()

        message_text = input("Введите сообщение для новых подписчиков: ")
        username = input('Введите свой логин без @:\n')
        print("Логин введён")

        # Загружаем известных подписчиков из файла
        known_followers = load_followers_from_file()

        while True:
            current_followers = follower_management_use_case.get_followers(username)
            # new_followers = current_followers - known_followers

            # for follower in new_followers:
            #     message_sending_use_case.send_message_to_follower(follower, message_text)

            # Обновляем список известных подписчиков и сохраняем в файл
            known_followers = current_followers
            save_followers_to_file(known_followers)

            print("Проверка завершена. Ожидание перед следующей проверкой...")
            time.sleep(300)  # Ждем 5 минут перед следующей проверкой

    except KeyboardInterrupt:
        print("Завершение работы...")
    except WebDriverException as e:
        print(f"Произошла ошибка WebDriver: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
