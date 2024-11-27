# use_cases/message_sending_use_case.py

from interfaces.web_interface import WebInterface
from entities.follower import Follower

class MessageSendingUseCase:
    def __init__(self, web_interface: WebInterface):
        self.web_interface = web_interface

    def send_message_to_follower(self, follower: Follower, message_text: str):
        self.web_interface.navigate_to(follower.profile_url)
        try:
            # Ищем кнопку для отправки сообщения
            locator_button = {"by": "xpath",
                              "value": "//div[contains(text(), 'Сообщение') or contains(text(), 'Message')]"}
            message_button = self.web_interface.wait_until_clickable(locator_button, timeout=10)
            self.web_interface.click_element(message_button)

            # Ожидаем появления окна чата и находим строку ввода
            locator_input = {"by": "xpath", "value": "//div[@contenteditable='true' and @role='textbox']"}
            message_input = self.web_interface.wait_until_present(locator_input, timeout=15)
            self.web_interface.click_element(message_input)

            # Проверка, что поле ввода готово
            if message_input.is_enabled():
                # Вводим сообщение
                message_input.send_keys(message_text)
                message_input.send_keys('\ue007')  # Нажимаем Enter
                print(f"Сообщение отправлено: {follower.username}")
            else:
                print(f"Поле ввода не доступно для пользователя {follower.username}")
        except Exception as e:
            print(f"Не удалось отправить сообщение {follower.username}: {str(e)}")


