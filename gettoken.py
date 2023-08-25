# рабочая штука, ждет пока пользователь залогинится и даст доступ, потом сразу забирает токен и закрывает браузер
# осталось наладить вариативность для разных браузеров

from selenium import webdriver
import re
# https://oauth.vk.com/authorize?client_id=51723957&display=page&scope=photos&response_type=token&v=5.131
def get_token(client_id):
    token = None
    id = None
    
    try:
        driver = webdriver.Chrome()
    except:
        try:
            driver = webdriver.Edge()
        except:
            print('Не, ну это уже не серьезно!')
  
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
        