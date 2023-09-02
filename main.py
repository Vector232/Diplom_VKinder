import vk_api_plus as vk
import usercardmaker as ucm
import database.vkinderdbselect as dbselect
import jsonwrite as jw
import loger
import matchmaker as mm
# это нужно будет убрать
from database.vkinderdbmodel import *
from pprint import pprint

#  Регулирует поиск и выдачу кандидатов.
def find_candidates(session, matchmaker, db, card, log=None):
    if log: log.log(f"Main -> Инициирован поиск кандидатов.")
    
    #  Получить прошлых кандидатов
    # viewed = db.get_viewed(card['user_id'])
    # print(f'Есть в БД: {viewed}')

    #  Зафиксировать просмотренные профили
    currently_viewed = {}
    candidates = {}

    #  Параметры поиска. Вынес чтобы можно было менять. Правило изменения не придумал.                  Придумай!!!
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
        if log: log.log(f"Main -> Запрос пре-кандидатов с параметрами: {fields}.")
        response = session.get(url=session.USERS_SEARCH, **fields).json()
        
        if len(response['response']['items']) == 0: break # дописать момент с изменение параметров поиска (для обхода ограниченией в 1000 профилей на выдаче) !!!!

        #  Проверяем пришел ли нужный ответ
        try:
            pre_candidates = response['response']['items']
        except Exception as ex:
            print(f'Main -> Возникла ошибочка в vk_api.find_candidates: {ex}\n Ответ: {response}')
            break
        
        #  Оцениваем полученных пре-кандидатов
        matchmaker.add_and_evaluation(pre_candidates)
        offset += count

    # print(currently_viewed)
    # viewed = DB.get_users()
    # print(f'Есть в БД после прохода: {viewed}')
    #  Эта часть только для лога и json-а.
    candidates = matchmaker.get_candidates(cut=False)
    if log: log.log(f"Main -> Подобрано {len(candidates)} кандидатов.")
    jw.write('Temp/candidates.json', candidates)
    return candidates

TEST = True

if __name__ == '__main__':
    print(f'{"НАЧАЛО РАБОТЫ ПРОГРАММЫ":*^31}')
    #  Создаем логер. Будет работать и без него. Но не сейчас.
    log = loger.Loger()

    #  Подрубаем базу данных.
    db = dbselect.DateBase(loger=log)

    #  Открываем сессию для работы с ВК ППИ. Без нее работать не будет.
    session = vk.VK_session(loger=log, test=TEST)
    
    #  Получаем токен.
    session.get_main_info()

    #  Получаем информацию о текущем пользователе.
    info = session.get_user_info(session.user_id, get_photo=True)
    #  Создаем карточку текущего пользователя.
    card, photos, was_noted = ucm.makeusercard(info, get_photo=True)

    # print(card)
    # for photo in photos:
    #     print(photo)
    # print(was_noted)
    
   
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

    #  Подрубаем искателя кандидатов.
    matchmaker = mm.Matchmaker(session, db, card, log, TEST)
    candidates = find_candidates(session=session, matchmaker=matchmaker, db=db, card=card, log=log)
    while input('Показать кандидатов?(y)') == 'y':
        candidates_ = matchmaker.get_candidates()
        for i in candidates_:
            print(i)
    # print(candidates)

    print(f'{"КОНЕЦ РАБОТЫ ПРОГРАММЫ":*^31}')