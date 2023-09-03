import vkapi.vk_api_plus as vk
import vkapi.usercardmaker as ucm
import database.vkinderdbselect as dbselect
import logs.jsonwrite as jw
import logs.loger as loger
import matchmaker as mm
import rule
# это нужно будет убрать
from database.vkinderdbmodel import *
from pprint import pprint

#  Регулирует поиск и выдачу кандидатов. Новая версия.
def find_candidates_2(session, matchmaker, db, card, log=None):
    if log: log.log(f"Main -> Инициирован поиск кандидатов.")
    candidates = {}

    if card['fields']['sex'] == 1: sex = 2
    elif card['fields']['sex'] == 2: sex = 1
    else: sex = None

    bdate = card['fields']['bdate']
    if bdate == None:
        age = input('Дата рождения не указана. Укажите год рождения для качественного поиска: ')
    else:
        bdate = int(bdate.split(sep='.')[-1])
        if bdate < 1902:
            age = input("Дата рождения указана без года. Укажите год для качественного поиска: ")
        else:
            age = bdate

    print('\n'*50)
    while True:
        print(f'{"Инструкция":-^50}')
        print(f'{"Для работы с программой введите команду.":-^50}')
        print(f'{"Список доступных команд доступен по команде <help>.":-^50}')
        print(f'В списке кандидатов нерассмотрены {len(matchmaker.candidates)} кандидатов.')
        command = input("Введите команду: ")

        if command == 'help':
            print('\n'*3)
            print(f'{"Список доступных команд:":-^50}')
            print(f'{"search -> найти кандидатов":-<50}')
            print(f'{"get -> вывести десятку лучших":-<50}')
            print(f'{"clear -> отчистить список кандидатов":-<50}')
            print(f'{"exit -> завершить работу":-<50}')
        elif command == 'exit':
            break
        elif command == 'search':
            fields = rule.rule(age, sex)
            if log: log.log(f"Main -> Запрос пре-кандидатов с параметрами: {fields}.")
            #  Запрашиваем список пре-кандидатов.
            response = session.get(url=session.USERS_SEARCH, **fields).json()

            #  Проверяем пришел ли нужный ответ
            try:
                pre_candidates = response['response']['items']
            except Exception as ex:
                print(f'Main -> Возникла ошибочка в vk_api.find_candidates: {ex}\n Ответ: {response}')
                break

            #  Оцениваем полученных пре-кандидатов
            matchmaker.add_and_evaluation(pre_candidates)
        elif command == 'get':
            candidates_ = matchmaker.get_candidates()
            jw.write('Temp/candidates.json', candidates_)
        elif command == 'clear':
            matchmaker.candidates = []



    #  Эта часть только для лога и json-а.
    candidates = matchmaker.get_candidates(cut=False)
    if log: log.log(f"Main -> Подобрано {len(candidates)} кандидатов.")
    jw.write('Temp/allcandidates.json', candidates)

    return


TEST = False

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

    #  Запускаем примитивный интерфейс через принты и инпуты
    find_candidates_2(session=session, matchmaker=matchmaker, db=db, card=card, log=log)

    print(f'{"КОНЕЦ РАБОТЫ ПРОГРАММЫ":*^31}')