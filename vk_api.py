import requests
import os
from pprint import pprint
from dotenv import load_dotenv
# самодельные модули с нужным функционалом
# работа с json файлами
import jsonwrite as jw
# получение токена вк
from gettoken import get_token
import loger


load_dotenv()

class VK_session:
    def __init__(self, env = False):
        self.log = loger.Loger()
        self.log.log("Создан объект класса VK_session.")

        self.version = 5.131
        self.users_search = 'https://api.vk.com/method/users.search'
        self.users_get = 'https://api.vk.com/method/users.get'
        self.photo_get = 'https://api.vk.com/method/photos.get'
        self.env = env

    # Получаем стартовые данные от пользователя и вытаскиваем токен для дальнейшей работы.
    def start(self):
        # для удобного тестирования
        if self.env:
            self.log.log("Сессия запущена в тестовом режиме. Данные получены из окружения.")
            
            print('Тестовый режим. Токен успешно получен!')
            self.user_id = os.getenv('USER_ID')
            self.access_token = os.getenv('USER_TOKEN')
            return
        
        self.log.log("Сессия запущена в основном режиме.")
        while True:
            try:
                (self.access_token, self.user_id) = get_token(os.getenv('CLIENT_ID'))
                if not self.access_token: raise Exception
                
                self.log.log(f"Токен успешно получен! Токен: {self.access_token}")
                self.log.log(f"Токен получен для пользователя с ID: {self.user_id}")
                print('Токен успешно получен!')
                print(f'Токен: {self.access_token}')
                break
            except:
                self.log.log("Неудачная попытка получения токена.")
                print('Нудалось получить токен! Проверьте правильность введенных логина и/или пароля!')

    
    def create_user_card(self, id, get_photo=False):

        def take_top3_photo(data):
            sorted_dict = sorted(data['response']['items'], key=lambda x: -x['likes']['count'] - x['comments']['count'])
            return sorted_dict[1:4]
        
        self.log.log(f"Создаем карточку пользователяю с ID: {id}")
        data = self.get(url=self.users_get, user_id=id, fields='sex, relation, city, bdate').json()

        if get_photo:
            data['photo'] = take_top3_photo(self.get(url=self.photo_get, owner_id=id, album_id='profile', extended=1).json())
            
        jw.write('Temp/data.json', data)


    # универсальная штука для коротких запросов к ППО ВК
    def get(self, url, **kwargs):
        self.log.log(f"Запрос к ППО ВК: {url}: ({kwargs})")
        params = {'access_token': self.access_token, 
                    'v': self.version,
                    **kwargs
                    }
        
        response = requests.get(url=url, params=params)

        return response
    

    def __del__(self):
        self.log.log('Сессия завершена!')


    def test1(self):
        response = self.get(url=self.users_search, q='', count=10)
        jw.write('Temp/data.json', response)
        pprint(jw.read('Temp/data.json'))
       