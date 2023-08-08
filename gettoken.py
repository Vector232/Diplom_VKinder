# рабочая штука, ждет пока пользователь залогинится и даст доступ, потом сразу забирает токен и закрывает браузер
# осталось наладить вариативность для разных браузеров

import os
from selenium import webdriver
import pyenv
import re

def get_token(id):
    pyenv.load_env()
   
    token = None

    driver = webdriver.Chrome()
  
    try:
        driver.maximize_window()
        driver.get(f'https://oauth.vk.com/authorize?client_id={id}&display=page&scope=photos&response_type=token&v=5.131')

        while True:
            url = driver.current_url
            if 'access_token' in url:
                patern = r'.*access_token=(.*)&expires_in.*'
                replace  = r'\1'
                token = re.sub(patern, replace, url)
                break

        driver.close()
        driver.quit()
        return token       
    except Exception as ex:
        token = None
        return token
        