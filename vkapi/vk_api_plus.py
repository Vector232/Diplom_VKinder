import requests
import os
from dotenv import load_dotenv
import time

#  Самодельные модули с нужным функционалом
#  Логер. Спасибо Кэп.
from logs.loger import Loger
#  Работа с json файлами
import logs.jsonwrite as jw
#  Получение токена вк
from vkapi.gettoken import get_token


class VK_session:
    # test - определяет режим работы. True: Тестовый берет данные из окружения.
    def __init__(self, loger: Loger = None, test = False):  
        load_dotenv()

        self.log = loger
        if self.log:
            self.log.log("VK_API -> Создан объект класса VK_session.")

        self.VERSION = 5.131
        self.USERS_SEARCH = 'https://api.vk.com/method/users.search'
        self.USERS_GET = 'https://api.vk.com/method/users.get'
        self.PHOTO_GET = 'https://api.vk.com/method/photos.get'
        self.PHOTO_GETUSERPHOTOS = 'https://api.vk.com/method/photos.getUserPhotos'
        self.test = test

    #  Получаем стартовые ДАННЫЕ от пользователя, 
    #  вытаскиваем токен для дальнейшей работы.
    def get_main_info(self):
        # для удобного тестирования
        if self.test:
            if self.log:
                self.log.log("VK_API -> Сессия запущена в тестовом режиме. Данные получены из окружения.")
            
            print('Тестовый режим. Токен успешно получен!')
            self.user_id = os.getenv('USER_ID')
            self.access_token = os.getenv('USER_TOKEN')
            return
        
        if self.log:
            self.log.log("VK_API -> Сессия запущена в основном режиме.")
        while True:
            try:
                (self.access_token, self.user_id) = get_token(os.getenv('CLIENT_ID'))
                if not self.access_token: 
                    raise Exception
                
                if self.log:
                    self.log.log(f"VK_API -> Токен успешно получен! Токен: {self.access_token}")
                    self.log.log(f"VK_API -> Токен получен для пользователя с ID: {self.user_id}")
                print('Токен успешно получен!')
                print(f'Токен: {self.access_token}')
                break
            except Exception as ex:
                if self.log:
                    self.log.log("VK_API -> Неудачная попытка получения токена.")
                    self.log.log(f"VK_API -> Exception: {ex}")
                print('Нудалось получить токен! Проверьте правильность введенных логина и/или пароля!')
                if input("Введите <break> для завершения работы программы: ") == 'break':
                    (self.access_token, self.user_id) = None, None
                    break

    
    def get_user_info(self, id, get_photo=False):
        #  На случай непредвиденных обстоятельств.
        if id is None:
            return None

        # получаем только три топовые фотографии
        def take_top3_photo(data):
            try:
                sorted_dict = sorted(data['response']['items'], 
                            key=lambda x: -x['likes']['count'] - x['comments']['count'])
            except: 
                print(f'{data}')
                raise
            # на случай если не набралось 3 фотки в профиле
            return sorted_dict[1:4] if len(sorted_dict) > 3 else sorted_dict 
        
        if self.log: 
            self.log.log(f"VK_API -> Создаем карточку пользователяю с ID: {id}")
        data = self.get(url=self.USERS_GET, 
                        user_id=id, 
                        fields='sex, relation, city, bdate'
                        ).json()

        if get_photo: 
            #  Фото берем из альбома с фото профиля.
            untested_data = self.get(url=self.PHOTO_GET,
                                    owner_id=id, 
                                    album_id='profile', 
                                    extended=1
                                    ).json()
            #  Если не приватный.
            if untested_data.get('error'): 
                return data

            data['photo'] = take_top3_photo(untested_data)
            
            #  Получаем фото на которых пользователь был отмечен
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
        if self.log: 
            self.log.log(f"VK_API -> Запрос к ППИ ВК: {url}: ({kwargs})")
        params = {'access_token': self.access_token, 
                    'v': self.VERSION,
                    **kwargs
                    }
        try:
            response = requests.get(url=url, params=params)
            time.sleep(0.3)
            if self.log: 
                self.log.log(f"VK_API -> Ответ от ППИ ВК: {response}")
        except Exception as ex:
            print(f'Возникла ошибочка в vk_api.get: {ex}')
            if self.log: 
                self.log.log(f"VK_API -> Возникла ошибочка в vk_api.get: {ex}")
        return response
    
    # def __del__(self):
    #     if self.log: self.log.log('Сессия завершена!')