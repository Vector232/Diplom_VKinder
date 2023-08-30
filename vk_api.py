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
# проверяет пре-кандидата на соответствие статусу кандидата
import matchmaker as mm
load_dotenv()

class VK_session:
    def __init__(self, test = False): # env - определяет режим работы. True: Тестовый берет данные из окружения. 
        self.log = loger.Loger()
        self.log.log("Создан объект класса VK_session.")

        self.VERSION = 5.131
        self.USERS_SEARCH = 'https://api.vk.com/method/users.search'
        self.USERS_GET = 'https://api.vk.com/method/users.get'
        self.PHOTO_GET = 'https://api.vk.com/method/photos.get'
        self.PHOTO_GETUSERPHOTOS = 'https://api.vk.com/method/photos.getUserPhotos'
        self.test = test

    # Получаем стартовые ДАННЫЕ от пользователя и вытаскиваем токен для дальнейшей работы.
    def start(self):
        # для удобного тестирования
        if self.test:
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
        data = self.get(url=self.USERS_GET, user_id=id, fields='sex, relation, city, bdate').json()

        if get_photo: 
            # фото берем из альбома с фото профиля
            data['photo'] = take_top3_photo(self.get(url=self.PHOTO_GET, owner_id=id, album_id='profile', extended=1).json())
            # получаем фото на которых пользователь был отмечен
            data['was_noted'] = self.get(url=self.PHOTO_GETUSERPHOTOS, user_id=id).json()['response']
            
        jw.write('Temp/data.json', data)

        return data
    
    # Находит 10 кандидатов по правилу.
    def find_candidates(self, db, card: dict):
        self.log.log(f"Инициирован поиск кандидатов.")
        # главный оцениватель пре-кандидатов
        matchmaker = mm.Matchmaker(db, card, self.log, self.test)

        # получить прошлых кандидатов
        # viewed = db.get_viewed(card['user_id'])
        # print(f'Есть в БД: {viewed}')

        # зафиксировать просмотренные профили
        self.currently_viewed = {}
        candidates = {}

        # параметры поиска
        query = ''
        offset = 0
        count = 50
        if card['fields']['sex'] == 1: sex = 2
        elif card['fields']['sex'] == 2: sex = 1
        else: sex = None

        while True:     
            fields = {'q': query,
                  'sort': 0,
                  'offset': offset,
                  'count': count,
                  'sex': sex,
                  'fields': 'bdate, sex, relation, city'}

            # запрашиваем список пре-кандидатов
            self.log.log(f"Запрос пре-кандидатов с параметрами: {fields}.")
            response = self.get(url=self.USERS_SEARCH, **fields).json()
            time.sleep(0.3) # подумать над заменой сна на что-то инное                  !!!!
            
            if len(response['response']['items']) == 0: break # дописать момент с изменение параметров поиска (для обхода ограниченией в 1000 профилей на выдаче)

            # проверяем пришел ли нужный ответ
            try:
                pre_candidates = response['response']['items']
            except Exception as ex:
                print(f'Возникла ошибочка в vk_api.find_candidates: {ex}\n Ответ: {response}')
                break
            
            # оцениваем полученных пре-кандидатов
            matchmaker.add_and_evaluation(pre_candidates)
            offset += count

        # print(currently_viewed)
        # viewed = DB.get_users()
        # print(f'Есть в БД после прохода: {viewed}')
        candidates = matchmaker.get_candidates(slice_=False)
        self.log.log(f"Подобрано {len(candidates)} кандидатов.")
        jw.write('Temp/candidates.json', candidates)
        return candidates
            


    # универсальная штука для коротких запросов к ППО ВК.
    # Источник исключения при невалидном токене.
    # Только в тестовом ломается из-за неактуального токена.
    # По идее невозможно в рабочем режиме. 
    def get(self, url, **kwargs):
        self.log.log(f"Запрос к ППО ВК: {url}: ({kwargs})")
        params = {'access_token': self.access_token, 
                    'v': self.VERSION,
                    **kwargs
                    }
        try:
            response = requests.get(url=url, params=params)
            self.log.log(f"Ответ от ППО ВК: {response}")
        except Exception as ex:
            print(f'Возникла ошибочка в vk_api.get: {ex}')
            self.log.log(f"Возникла ошибочка в vk_api.get: {ex}")
        return response
    

    def __del__(self):
        self.log.log('Сессия завершена!')

    # пусть будет тут какое-то время
    def test1(self):
        response = self.get(url=self.users_search, q='', count=10, city=None)
        jw.write('Temp/data.json', response)
        pprint(jw.read('Temp/data.json'))
       