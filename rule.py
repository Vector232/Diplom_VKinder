#  Правило формирования запроса к ППИ VK для обхода ограничений в 1000 пользователей для users.search
import random

def rule(age, sex):
    query = 'ЁЙЦУКЕНГШЩЗХФЫВАПРОЛДЖЭЯЧСМИТБЮQWERTYUIOPASDFGHJKLZXCVBNM '

    fields = {  'q': random.sample(query, 1),
                'sex': sex,
                'fields': 'bdate, sex, relation, city',
                'age_from': age - 6,
                'age_to': age + 6}
    
    return fields

if __name__ == '__main__':  
    for _ in range(10):
        print(rule(age=2000, sex=2))