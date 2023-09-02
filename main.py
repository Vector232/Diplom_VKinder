import time

import vk_api_plus as vk
import usercardmaker as ucm
import database.vkinderdbselect as dbselect
import jsonwrite as jw
import loger
import matchmaker as mm
# это нужно будет убрать
from database.vkinderdbmodel import *
from pprint import pprint

#  Находит 10 кандидатов по правилу.
def find_candidates(self, matchmaker, db, card, log=None):
    if log: log.log(f"Инициирован поиск кандидатов.")
    #  Главный оцениватель пре-кандидатов
    

    #  Получить прошлых кандидатов
    # viewed = db.get_viewed(card['user_id'])
    # print(f'Есть в БД: {viewed}')

    #  Зафиксировать просмотренные профили
    currently_viewed = {}
    candidates = {}

    #  Параметры поиска
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

        #  Запрашиваем список пре-кандидатов
        if log: log.log(f"Запрос пре-кандидатов с параметрами: {fields}.")
        response = self.get(url=self.USERS_SEARCH, **fields).json()
        time.sleep(0.3) # подумать над заменой сна на что-то инное                  !!!!
        
        if len(response['response']['items']) == 0: break # дописать момент с изменение параметров поиска (для обхода ограниченией в 1000 профилей на выдаче) !!!!

        #  Проверяем пришел ли нужный ответ
        try:
            pre_candidates = response['response']['items']
        except Exception as ex:
            print(f'Возникла ошибочка в vk_api.find_candidates: {ex}\n Ответ: {response}')
            break
        
        #  Оцениваем полученных пре-кандидатов
        matchmaker.add_and_evaluation(pre_candidates)
        offset += count

    # print(currently_viewed)
    # viewed = DB.get_users()
    # print(f'Есть в БД после прохода: {viewed}')
    #  Эта часть только для лога и json-а.
    candidates = matchmaker.get_candidates(cut=False)
    if log: log.log(f"Подобрано {len(candidates)} кандидатов.")
    jw.write('Temp/candidates.json', candidates)
    return candidates

TEST = True

if __name__ == '__main__':
    print(f'{"НАЧАЛО РАБОТЫ ПРОГРАММЫ":*^31}')
    #  Создаем логер. Будет работать и без него. Но не сейчас.
    log = loger.Loger()

    #  Открываем сессию для работы с ВК ППИ. Без нее работать не будет.
    session = vk.VK_session(loger=log, test=TEST)
    
    # Получаем токен.
    session.get_main_info()

    info = session.get_user_info(session.user_id, get_photo=True)
    
    card, photos, was_noted = ucm.makeusercard(info, get_photo=True)

    # print(card)
    # for photo in photos:
    #     print(photo)
    # print(was_noted)
    db = dbselect.DateBase()
   
    db.push(card)
    for photo in photos:
        db.push(photo)
    for photo in was_noted:
        db.push(photo)

    # q = db.session.query(User)
    # for i in q:
    #     print(i)

    # q = db.session.query(Photo)
    # for i in q:
    #     print(i)
    matchmaker = mm.Matchmaker(db, card, log, TEST)
    candidates = find_candidates(self=session, mm=matchmaker, db=db, card=card, log=log)

    candidates_ = session.matchmaker.get_candidates()
    for i in candidates_:
        print(i)
    # print(candidates)

    print(f'{"КОНЕЦ РАБОТЫ ПРОГРАММЫ":*^31}')