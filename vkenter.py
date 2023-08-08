import json
import requests
import webbrowser
import os
from pprint import pprint
import pyenv
import jsonwrite as jw
from gettoken import get_token
pyenv.load_env()

class VK_session:
    def __init__(self, env = False):
        self.version = 5.131
        self.users_search = 'https://api.vk.com/method/users.search'
        self.users_get = 'https://api.vk.com/method/users.get'
        self.env = env

    def start(self):
        if self.env:
            self.id = os.environ['ID']
            self.access_token = os.environ['USER_TOKEN']
            return
        
        print('Введите ID пользователя: ')
        while True:
            try:
                self.id = int(input())
                if self.id == -1: break

                self.access_token = get_token(self.id)
                if not self.access_token: raise Exception

                print('Токен успешно получен!')
                print(f'Токен: {self.access_token}')
                break
            except:
                print('Нудалось получить токен. Попробуйте другой ID или проверьте правильность введенных логина и/или пароля!')

    def get(self, url, **kwargs):
        params = {'access_token': self.access_token, 
                    'v': self.version,
                    **kwargs
                    }
        
        response = requests.get(url=url, params=params)

        return response


    def test1(self):
        response = self.get(url=self.users_search, q='', count=5)
        jw.write('data.json', response)
        pprint(jw.read('data.json'))
       

if __name__ == '__main__':
    session = VK_session()
    session.start()