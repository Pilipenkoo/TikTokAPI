# frameworks_and_drivers/follower_file_manager.py
import logging
import os
import json
from entities.follower import Follower

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def save_followers_to_file(followers, filename='followers.json'):
    print(f"Количество подписчиков: {len(followers)}")
    followers_list = [{'username': follower.username, 'profile_url': follower.profile_url} for follower in followers]

    # Сохранение в файл
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(followers_list, file, ensure_ascii=False, indent=4)

    # Логирование успешного сохранения
    logging.info("Подписчики сохранены в файл '%s'", filename)

def load_followers_from_file(filename='followers.json'):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            followers_list = json.load(file)
            return set(Follower(item['username'], item['profile_url']) for item in followers_list)
    else:
        return set()
