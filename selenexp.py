# рабочая штука, ждет пока пользователь залогинится и даст доступ, потом сразу забирает токен и закрывает браузер
# осталось наладить вариативность для разных браузеров

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pyenv
import re

pyenv.load_env()
id = 51723957
token = None

driver = webdriver.Chrome()
try:
    driver.maximize_window()
    driver.get(f'https://oauth.vk.com/authorize?client_id=51723957&display=page&scope=photos&response_type=token&v=5.131')
    time.sleep(5)

    while True:
        url = driver.current_url
        if 'access_token' in url:
            patern = r'.*access_token=(.*)&expires_in.*'
            replace  = r'\1'
            token = re.sub(patern, replace, url)
            print(token)
            break

except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()