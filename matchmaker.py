# card_f = {    'name': 'Владислав', 
#               'last_name': 'Троян', 
#               'bdate': '26.3.1902', 
#               'sex': 2, 
#               'relation': 0, 
#               'city': None
#                   добавить партнера
# }
# pre_candidat_f 

from logs.loger import Loger
import vkapi.usercardmaker as ucm
import logs.jsonwrite as jw

class Matchmaker():
    def __init__(self, session, db, card, log: Loger = None, test = False) -> None: # полностью результат usercardmaker-а
        self.log = log
        if self.log: 
            self.log.log("Matchmaker -> Matchmaker инициирован!")
        self.db = db
        self.session = session
        self.candidates = jw.read('Temp/allcandidates.json')
        #  Просмотренные в текущей сессии не будут рассматриваться в ней повторно.
        self.viewed = {}

        if test: # для тестовой работы
            self.card = {'model': 'user', 
                         'fields': {'user_id': 95135266, 
                                    'name': 'Владислав', 
                                    'last_name': 'Троян', 
                                    'bdate': '26.3.2000', 
                                    'sex': 2, 
                                    'relation': 0, 
                                    'city': 'Симферополь'
                                    }
                            }
        else:
            self.card = card

    def add_and_evaluation(self, precandidate_pool):
        blacklist = self.db.get_blacklist(id=self.card['fields']['user_id'])
        selected = []

        if self.log: 
            self.log.log(f"Matchmaker -> Matchmaker рассматривает {len(precandidate_pool)} пре-кандидатов.")
        for precandidat in precandidate_pool:
            #  Проверка на черный список и повторное вхождение в сессию.
            pc_id = precandidat.get('id')
            if pc_id in self.viewed or pc_id in blacklist:
                if self.log: 
                    self.log.log(f"Matchmaker -> Matchmaker пре-кандидат {pc_id} забанен или уже просмотрен в этой сессии.")
                continue

            grade = 0
            self.viewed[pc_id] = grade

            pc_sex = precandidat.get('sex', None)
            user_sex = self.card['fields']['sex']
            pc_relation = precandidat.get('relation', None)
            pc_relation_partner = precandidat.get('relation_partner', {'ans': False})
            user_bdate = self.card['fields']['bdate']
            pc_bdate = precandidat.get('bdate', None)

            #  Нужен только кандидат противоположного пола или любой, если пол user-а не указан
            if (user_sex == pc_sex and user_sex != 0) \
                or (user_sex != pc_sex and pc_sex == 0):
                    if self.log: 
                        self.log.log(f'Matchmaker -> Пре-кандидат {precandidat["id"]} не подошел по полу. {user_sex} и {pc_sex}')
                    continue
            
            # исключаем прекандидатов в браке
            if pc_relation == 4 or pc_relation == 8:
                if self.log: 
                    self.log.log(f'Matchmaker -> Пре-кандидат {precandidat["id"]} уже в браке.')
                continue

            # если у кого-то возраст не указан то пропускаем оценку по возрасту
            if pc_bdate is None or user_bdate is None:
                if self.log: 
                    self.log.log(f'Matchmaker -> Пре-кандидат {precandidat["id"]} не подошел. Не указан возраст.')
                continue
            
            # если у кого-то возраст указан без года то пропускаем оценку по возрасту
            user_bdate = int(user_bdate.split(sep='.')[-1])
            pc_bdate = int(pc_bdate.split(sep='.')[-1])
            if pc_bdate < 1902 or user_bdate < 1902:
                if self.log: 
                    self.log.log(f'Matchmaker -> Пре-кандидат {precandidat["id"]} не подошел. Полный возраст не указан.')
                continue

            # print(self.card)
            # нужен кандидат с определенным семейным положением
            # если в активном поиске или уже связан с user-ом, то 9 балла к оценке
            if pc_relation == 6 \
                or ((pc_relation == 7 \
                    or pc_relation == 3\
                    or pc_relation == 2)
                and pc_relation_partner.get('id') == self.card['fields']['user_id']):
                grade += 9
            # остальные варианты получают меньше баллов
            elif pc_relation == 1 or pc_relation == 0: 
                grade += 6 
            elif pc_relation is None:
                grade += 3
            else:
                if self.log: 
                    self.log.log(f'Matchmaker -> Пре-кандидат {precandidat["id"]} не подошел. Связан с другим партнером.')
                continue

            # оцениваем возраст
            difference = user_bdate - pc_bdate
            if user_sex is None:
                abs_dif = abs(difference)
                if abs_dif <= 2:
                    grade += 6
                elif abs_dif <= 4:
                    grade += 4
                elif abs_dif <= 5:
                    grade += 2
                else:
                    if self.log: 
                        self.log.log(f'Matchmaker -> Пре-кандидат {precandidat["id"]} не подошел. Неподходящий возраст для N.')
                    continue
            elif user_sex == 1:
                if 2 <= difference <= 4:
                    grade += 6
                elif 0 <= difference <= 5:
                    grade += 4
                elif -1 <= difference <= 6:
                    grade += 2
                else:
                    if self.log: 
                        self.log.log(f'Matchmaker -> Пре-кандидат {precandidat["id"]} не подошел. Неподходящий возраст для Ж.')
                    continue
            elif user_sex == 2:
                if -2 >= difference >= -3:
                    grade += 6
                elif -1 >= difference >= -4:
                    grade += 4
                elif difference == 0:
                    grade += 2
                else:
                    if self.log: 
                        self.log.log(f'Matchmaker -> Пре-кандидат {precandidat["id"]} не подошел. Неподходящий возраст для М.')
                    continue

            #  Если из одного города, то + 5 балла.
            user_city = self.card['fields']['city']
            pc_city = precandidat.get('city', None)
            if user_city == pc_city is not None:
                grade += 5

            self.viewed[pc_id] = grade

            if self.log: 
                self.log.log(f'Matchmaker -> Пре-кандидат {precandidat["id"]} прошел оценивание на {grade} баллов.')
            selected.append({'grade': grade, 'fields': precandidat})
        self.candidates.extend(selected)
        self.candidates.sort(reverse=True, key=lambda x: x['grade'])
        if self.log: 
            self.log.log(f'Matchmaker -> Прошли {len(selected)} кандидатов. Всего в пуле {len(self.candidates)} кандидатов.')


    def get_candidates(self, cut = True):
        if not cut:
            return self.candidates

        if len(self.candidates) >= 10:
            ans = self.candidates[:10]
            self.candidates = self.candidates[10:]
        else:
            ans = self.candidates
            self.candidates = []
        
        #  Заполняем БД, чтобы не забывать кого уже показывали.
        for candidate in ans:
            #  Создаем карточки кандидатов.
            info = self.session.get_user_info(candidate['fields']['id'], get_photo=True)
            card, photos, was_noted = ucm.makeusercard(info, get_photo = True)
            #  Создаем запись с карточкой кандидата.
            self.db.push(card)
            #  Создаем записи с фото кандидата.
            for photo in photos:
                self.db.push(photo)
            #  Создаем записи с фото где был отмечен кандидат.
            for photo in was_noted:
                self.db.push(photo)
            #  Создаем записи о выдаче карточки текущему пользователю.
            data = {'model': 'output', 
                    'fields': {'input_user_id': self.card['fields']['user_id'], 
                                'output_user_id': candidate['fields']['id'],
                                'grade': candidate['grade']
                                }
                    }
            self.db.push(data)
        
        return ans
    
    # def __del__(self):
    #     if self.log: self.log.log('Matchmaker завершил работу!')