import requests
import os
from pprint import pprint
from dotenv import load_dotenv
import time

#  Самодельные модули с нужным функционалом
#  Логер. Спасибо Кэп.
from loger import Loger
#  Работа с json файлами
import jsonwrite as jw
#  Получение токена вк
from vkapi.gettoken import get_token


class VK_session:
    def __init__(self, loger: Loger = None, test = False): # env - определяет режим работы. True: Тестовый берет данные из окружения. 
        load_dotenv()

        self.log = loger
        if self.log: self.log.log("VK_API -> Создан объект класса VK_session.")

        self.VERSION = 5.131
        self.USERS_SEARCH = 'https://api.vk.com/method/users.search'
        self.USERS_GET = 'https://api.vk.com/method/users.get'
        self.PHOTO_GET = 'https://api.vk.com/method/photos.get'
        self.PHOTO_GETUSERPHOTOS = 'https://api.vk.com/method/photos.getUserPhotos'
        self.test = test

    #  Получаем стартовые ДАННЫЕ от пользователя, вытаскиваем токен для дальнейшей работы.
    def get_main_info(self):
        # для удобного тестирования
        if self.test:
            if self.log: self.log.log("VK_API -> Сессия запущена в тестовом режиме. Данные получены из окружения.")
            
            print('Тестовый режим. Токен успешно получен!')
            self.user_id = os.getenv('USER_ID')
            self.access_token = os.getenv('USER_TOKEN')
            return
        
        if self.log: self.log.log("VK_API -> Сессия запущена в основном режиме.")
        while True:
            try:
                (self.access_token, self.user_id) = get_token(os.getenv('CLIENT_ID'))
                if not self.access_token: raise Exception
                
                if self.log: self.log.log(f"VK_API -> Токен успешно получен! Токен: {self.access_token}")
                if self.log: self.log.log(f"VK_API -> Токен получен для пользователя с ID: {self.user_id}")
                print('Токен успешно получен!')
                print(f'Токен: {self.access_token}')
                break
            except:
                if self.log: self.log.log("VK_API -> Неудачная попытка получения токена.")
                print('Нудалось получить токен! Проверьте правильность введенных логина и/или пароля!')

    
    def get_user_info(self, id, get_photo=False):
        # получаем только три топовые фотографии
        def take_top3_photo(data):
            try:
                sorted_dict = sorted(data['response']['items'], key=lambda x: -x['likes']['count'] - x['comments']['count'])
            except: # Возникает только в тестовом режиме при неактуальном токене. Надеюсь.
                print(f'Обнови токен в .env!')
                raise
            return sorted_dict[1:4]
        
        if self.log: self.log.log(f"VK_API -> Создаем карточку пользователяю с ID: {id}")
        data = self.get(url=self.USERS_GET, user_id=id, fields='sex, relation, city, bdate').json()

        if get_photo: 
            # фото берем из альбома с фото профиля
            data['photo'] = take_top3_photo(self.get(url=self.PHOTO_GET, owner_id=id, album_id='profile', extended=1).json())
            # получаем фото на которых пользователь был отмечен
            sub_data = self.get(url=self.PHOTO_GETUSERPHOTOS, user_id=id).json()
            if sub_data.get('response', False):
                data['was_noted'] = sub_data['response']
            else:
                data['was_noted'] = {}
            
        jw.write('Temp/data.json', data)

        return data        


    #  Универсальная штука для коротких запросов к ППО ВК.
    #  Источник исключения при невалидном токене.
    #  Только в тестовом ломается из-за неактуального токена.
    #  По идее невозможно в рабочем режиме. 
    def get(self, url, **kwargs):
        if self.log: self.log.log(f"Запрос к ППО ВК: {url}: ({kwargs})")
        params = {'access_token': self.access_token, 
                    'v': self.VERSION,
                    **kwargs
                    }
        try:
            response = requests.get(url=url, params=params)
            time.sleep(0.3)
            if self.log: self.log.log(f"VK_API -> Ответ от ППО ВК: {response}")
        except Exception as ex:
            print(f'Возникла ошибочка в vk_api.get: {ex}')
            if self.log: self.log.log(f"VK_API -> Возникла ошибочка в vk_api.get: {ex}")
        return response
    

    # def __del__(self):
    #     if self.log: self.log.log('Сессия завершена!')