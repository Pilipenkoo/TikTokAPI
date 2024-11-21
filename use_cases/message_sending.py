# use_cases/message_sending_use_case.py

from interfaces.web_interface import WebInterface
from entities.follower import Follower

class MessageSendingUseCase:
    def __init__(self, web_interface: WebInterface):
        self.web_interface = web_interface

    def send_message_to_follower(self, follower: Follower, message_text: str):
        self.web_interface.navigate_to(follower.profile_url)
        try:
            locator_button = {"by": "xpath", "value": "//button[contains(text(), 'Сообщение') or contains(text(), 'Message')]"}

            message_button = self.web_interface.wait_until_clickable(locator_button, timeout=10)
            self.web_interface.click_element(message_button)

            # Ожидаем появления окна чата
            locator_input = {"by": "xpath", "value": "//div[contains(@class, 'chat-input')]/p"}
            message_input = self.web_interface.wait_until_present(locator_input, timeout=10)
            self.web_interface.click_element(message_input)
            message_input.send_keys(message_text)
            message_input.send_keys('\ue007')  # Нажимаем Enter
            print(f"Сообщение отправлено: {follower.username}")
        except Exception:
            print(f"Не удалось отправить сообщение {follower.username}")
