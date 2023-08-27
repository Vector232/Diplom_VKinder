import requests
import os
import time
import string
from pprint import pprint
from dotenv import load_dotenv
# самодельные модули с нужным функционалом
# работа с json файлами
import jsonwrite as jw
# получение токена вк
from gettoken import get_token
import loger
# взаимодействие с БД
import database.vkinderdbselect as db
# собирает карточку пользователя
import usercardmaker as ucm
load_dotenv()

class VK_session:
    def __init__(self, env = False): # env - определяет режим работы. True: Тестовый берет данные из окружения. 
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

    
    def get_user_info(self, id, get_photo=False):
        # получаем только три топовые фотографии
        def take_top3_photo(data):
            sorted_dict = sorted(data['response']['items'], key=lambda x: -x['likes']['count'] - x['comments']['count'])
            return sorted_dict[1:4]
        
        self.log.log(f"Создаем карточку пользователяю с ID: {id}")
        data = self.get(url=self.users_get, user_id=id, fields='sex, relation, city, bdate').json()

        if get_photo: # фото берем из альбома с фото профиля
            data['photo'] = take_top3_photo(self.get(url=self.photo_get, owner_id=id, album_id='profile', extended=1).json())
            
        jw.write('Temp/data.json', data)

        return data
    
    # Находит 10 кандидатов по правилу.
    def find_candidates(self, DB, card: dict):
        # получить прошлых кандидатов
        viewed = DB.get_viewed(card['user_id'])
        print(f'Есть в БД: {viewed}')
        #  зафиксировать просмотренные профили
        currently_viewed = {}
        candidates = {}
        # alphabet = [chr(i) for i in range('a','a'+32)] + string.ascii_uppercase
        query = ''
        offset = 0
        count = 50
        sex = card['fields'].get('sex', 0)
        
        while len(candidates) < 10:         
            print(f'Новый проход {count} {offset}')
            if offset >= 900: break

            fields = {'q': query,
                  'sort': 0,
                  'offset': offset,
                  'count': count,
                  'sex': sex,
                  'fields': 'bdate, sex, relation, city'}
            
            response = self.get(url=self.users_search, **fields).json()
            time.sleep(0.3)
            try:
                pre_candidates = response['response']['items']
            except:
                print(response)
                break
            #нужно написать правило подбора. Пожалуй самая тяжелая часть.
            for pre_candidat in pre_candidates:
                currently_viewed[pre_candidat['id']] = True

                bdate_a = pre_candidat.get('bdate', None)
                if bdate_a != None: bdate_a = int(bdate_a.split(sep='.')[-1])
                else: continue
                bdate_b = card['fields'].get('age')
                if bdate_a > 2003:
                    candidates[pre_candidat['id']] = ucm.makeusercard({'response':[pre_candidat]})
                    DB.push_user_card(candidates[pre_candidat['id']])
                    
                    if len(candidates) >= 10:
                        break

            offset += 50
        print(currently_viewed)
        viewed = DB.get_users()
        print(f'Есть в БД после прохода: {viewed}')
        return candidates
            


    # универсальная штука для коротких запросов к ППО ВК.
    # Источник исключения при невалидном токене.
    # Только в тестовом ломается из-за неактуального токена.
    # По идее невозможно в рабочем режиме. 
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
        response = self.get(url=self.users_search, q='', count=10, city=None)
        jw.write('Temp/data.json', response)
        pprint(jw.read('Temp/data.json'))
       