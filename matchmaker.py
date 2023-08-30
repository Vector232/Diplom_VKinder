# card_f = {    'name': 'Владислав', 
#               'last_name': 'Троян', 
#               'bdate': '26.3.1902', 
#               'sex': 2, 
#               'relation': 0, 
#               'city': None
#                   добавить партнера
# }
# pre_candidat_f  
import loger

class Matchmaker():
    def __init__(self, db, card, log: loger.Loger, test = False) -> None: # полностью результат usercardmaker-а
        self.log = log
        self.log.log(f"Matchmaker инициирован!")

        self.candidates = []
        
        if test: # для тестовой работы
            self.card = {'model': 'user', 'user_id': 95135266,'fields': {'name': 'Владислав', 'last_name': 'Троян', 'bdate': '26.3.2000', 'sex': 2, 'relation': 0, 'city': 'Симферополь'}}
        else:
            self.card = card

    def add_and_evaluation(self, precandidate_pool):
        viewed = {}
        selected = []
        self.log.log(f"Matchmaker рассматривает {len(precandidate_pool)} пре-кандидатов.")
        for precandidat in precandidate_pool:
            # на случай работы с ответами на разные заапросы к ППО ВК
            pc_id = precandidat.get('id')
            if pc_id in viewed: continue
            viewed[pc_id] = 0

            grade = 0
            
            pc_sex = precandidat.get('sex', None)
            user_sex = self.card['fields']['sex']
            pc_relation = precandidat.get('relation', None)
            pc_relation_partner = precandidat.get('relation_partner', {'ans': False})
            user_bdate = self.card['fields']['bdate']
            pc_bdate = precandidat.get('bdate', None)

            #  Нужен только кандидат противоположного пола или любой, если пол user-а не указан
            if (user_sex == pc_sex and user_sex != 0) \
                or (user_sex != pc_sex and pc_sex == 0):
                    self.log.log(f'Пре-кандидат {precandidat["id"]} не подошел по полу. {user_sex} и {pc_sex}')
                    continue
            
            # исключаем прекандидатов в браке
            if pc_relation == 4 or pc_relation == 8:
                self.log.log(f'Пре-кандидат {precandidat["id"]} уже в браке.')
                continue

            # если у кого-то возраст не указан то пропускаем оценку по возрасту
            if pc_bdate == None or user_bdate == None:
                self.log.log(f'Пре-кандидат {precandidat["id"]} не подошел. Не указан возраст.')
                continue
            
            # если у кого-то возраст указан без года то пропускаем оценку по возрасту
            user_bdate = int(pc_bdate.split(sep='.')[-1])
            pc_bdate = int(pc_bdate.split(sep='.')[-1])
            if pc_bdate < 1902 or user_bdate < 1902:
                self.log.log(f'Пре-кандидат {precandidat["id"]} не подошел. Полный возраст не указан.')
                continue

            # print(self.card)
            # нужен кандидат с определенным семейным положением
            # если в активном поиске или уже связан с user-ом, то 9 балла к оценке
            if pc_relation == 6 \
                or ((pc_relation == 7 \
                    or pc_relation == 3\
                        or pc_relation == 2) and pc_relation_partner.get('id') == self.card['user_id']):
                grade += 9
            # остальные варианты получают меньше баллов
            elif pc_relation == 1 or pc_relation == 0: 
                grade += 6 
            elif pc_relation == 1 or pc_relation == 0:
                grade += 3
            else:
                self.log.log(f'Пре-кандидат {precandidat["id"]} не подошел. Связан с другим партнером.')
                continue


            # оцениваем возраст
            difference = user_bdate - pc_bdate
            if user_sex == None:
                abs_dif = abs(difference)
                if abs_dif <= 2:
                    grade += 6
                elif abs_dif <= 4:
                    grade += 4
                elif abs_dif <= 5:
                    grade += 2
                else:
                    self.log.log(f'Пре-кандидат {precandidat["id"]} не подошел. Неподходящий возраст.')
                    continue
            elif user_sex == 1:
                if 2 <= difference <= 4:
                    grade += 6
                elif 0 <= difference <= 5:
                    grade += 4
                elif -1 <= difference <= 6:
                    grade += 2
                else:
                    self.log.log(f'Пре-кандидат {precandidat["id"]} не подошел. Неподходящий возраст.')
                    continue
            elif user_sex == 2:
                if -2 >= difference >= -3:
                    grade += 6
                elif -1 >= difference >= -4:
                    grade += 4
                elif difference == 0:
                    grade += 2
                else:
                    self.log.log(f'Пре-кандидат {precandidat["id"]} не подошел. Неподходящий возраст.')
                    continue
            
            # Если из одного города, то + 2 балла
            user_city = self.card['fields']['city']
            pc_city = precandidat.get('city', None)
            if user_city == pc_city != None:
                grade += 2

            viewed[pc_id] = grade

            self.log.log(f'Пре-кандидат {precandidat["id"]} прошел оценивание на {grade} баллов.')
            selected.append({'grade': grade, 'fields': precandidat})
        self.candidates.extend(selected)
        self.candidates.sort(reverse=True, key=lambda x: x['grade'])
        self.log.log(f'Прошли {len(selected)} кандидатов. Всего в пуле {len(self.candidates)} кандидатов.')


    def get_candidates(self, slice_ = True):
        if not slice_: return self.candidates

        if len(self.candidates) >= 10:
            ans = self.candidates[:10]
            self.candidates = self.candidates[10:]
            return ans
        else:
            return self.candidates
    
    def __del__(self):
        self.log.log('Matchmaker завершил работу!')

                

            
# устарело
def is_candidate(card_f, pre_candidat_f, env):
    # print(pre_candidat_f)
    user_bdate = int(card_f['bdate'].split(sep='.')[-1])
    pre_cand_bdate = pre_candidat_f.get('bdate', None)
   
    if pre_cand_bdate == None: return False
    # print(user_bdate - int(pre_cand_bdate.split(sep='.')[-1]))
    if 1 < (user_bdate - int(pre_cand_bdate.split(sep='.')[-1])) < 4:
        return True
    return False