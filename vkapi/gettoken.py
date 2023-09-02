# рабочая штука, ждет пока пользователь залогинится и даст доступ, потом сразу забирает токен и закрывает браузер
# осталось наладить вариативность для разных браузеров
# https://oauth.vk.com/authorize?client_id=51723957&display=page&scope=photos&response_type=token&v=5.131

import re

from selenium import webdriver


def get_token(client_id):
    token = None
    id = None
    
    
    driver = webdriver.Edge()
        
  
    try:
        driver.maximize_window()
        driver.get(f'https://oauth.vk.com/authorize?client_id={client_id}&display=page&scope=photos&response_type=token&v=5.131')

        while True:
            url = driver.current_url
            if 'access_token' in url:
                patern = r'.*access_token=(.*)&expires_in.*user_id=(.*)'
                replace_token  = r'\1'
                replace_id = r'\2'
                token = re.sub(patern, replace_token, url)
                id = re.sub(patern, replace_id, url)
                break

        driver.close()
        driver.quit()
        return token, id    
    except Exception as ex:
        print(ex)
        token = None
        id = None
        return token, id
        