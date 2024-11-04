import os
import pickle
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

# Загружаем cookies из файла, если он существует
def load_cookies(driver, cookies_file='tiktok_cookies.pkl'):
    if os.path.exists(cookies_file) and os.path.getsize(cookies_file) > 0:
        try:
            with open(cookies_file, 'rb') as file:
                cookies = pickle.load(file)
                for cookie in cookies:
                    driver.add_cookie(cookie)
        except EOFError:
            print("Файл с куками поврежден. Пропускаем загрузку куки.")
    else:
        print("Файл с куками не найден или пуст, требуется новая авторизация.")

# Сохраняем cookies в файл для последующего использования
def save_cookies(driver, cookies_file='tiktok_cookies.pkl'):
    with open(cookies_file, 'wb') as file:
        pickle.dump(driver.get_cookies(), file)

# Проверка, залогинен ли пользователь
def is_logged_in(driver):
    return "Войти" not in driver.page_source

# Авторизация через Google, если это необходимо
def login(driver):
    driver.get('https://www.tiktok.com/login')
    try:
        google_login_button = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Продолжить с Google')]"))
        )
        google_login_button.click()
    except TimeoutException:
        print("Не удалось найти элемент для входа через Google.")
    input("После входа введите любой символ и нажмите Enter...")
    save_cookies(driver)

# Получение списка подписчиков
def get_followers(driver, username):
    driver.get(f'https://www.tiktok.com/@{username}/followers')
    time.sleep(5)  # Ожидание загрузки списка подписчиков
    followers = driver.find_elements(By.XPATH, "//a[@class='user-info']")  # Убедитесь, что XPATH актуален
    return {follower.get_attribute("href") for follower in followers}

# Отправка сообщения новому подписчику
def send_message_to_follower(driver, follower_url, message_text):
    driver.get(follower_url)
    try:
        message_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Message')]"))
        )
        message_button.click()
        message_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//textarea"))
        )
        message_input.send_keys(message_text)
        message_input.send_keys(Keys.RETURN)
        print(f"Сообщение отправлено новому подписчику: {follower_url}")
    except TimeoutException:
        print(f"Не удалось отправить сообщение {follower_url}")

# Основная функция для запуска процесса
def main():
    driver_path = 'chromedriver.exe'
    service = Service(driver_path)
    options = Options()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--start-maximized')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get('https://www.tiktok.com/')

    # Загружаем cookies и обновляем страницу
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    load_cookies(driver)
    driver.refresh()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

    # Если не залогинены, выполняем вход
    if not is_logged_in(driver):
        login(driver)

    message_text = input("Введите сообщение для новых подписчиков: ")
    username = input('Введите свой логин без @:\n')
    known_followers = get_followers(driver, username)

    try:
        # Цикл для регулярной проверки новых подписчиков
        while True:
            time.sleep(60)  # Проверка новых подписчиков каждую минуту
            current_followers = get_followers(driver, username)
            new_followers = current_followers - known_followers
            for follower_url in new_followers:
                send_message_to_follower(driver, follower_url, message_text)
            known_followers = current_followers
    except KeyboardInterrupt:
        print("Завершение работы...")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
