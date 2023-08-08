import json
import requests
import webbrowser
import os
from pprint import pprint
import pyenv
import jsonwrite as jw
pyenv.load_env()

class VK_session:
    def __init__(self):
        self.version = 5.131
        self.users_search = 'https://api.vk.com/method/users.search'
        self.users_get = 'https://api.vk.com/method/users.get'
        self.access_token = os.environ['USER_TOKEN']

    def start(self):
        while True:
            try:
                self.id = int(input())
                self.access_token = self.take_access_token()
                break
            except:
                print('Некорректный id!')

    
    def take_access_token(self, id):

        url = f'https://oauth.vk.com/authorize?client_id=51723957&display=page&scope=photos&response_type=token&v=5.131'
        response = requests.get(url=url).json()
        pprint(response)
        pass


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
    # session.start()
    # session.test1()
    session.take_access_token(51723957)