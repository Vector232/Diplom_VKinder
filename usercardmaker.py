# заполняет крточку пользователя
from datetime import datetime


def makeusercard(dict_: dict) -> dict:
    def in_age(bdate: str) -> int:
        if not bdate: return -1 

        a = datetime.now().year
        b = int(bdate.split(sep='.')[2])

        return a - b
    
    source = dict_["response"][0]

    best_data = {}
    best_data['model'] = 'user'
    best_data['user_id'] = source.get("id", -1)
    best_data['fields'] = {}
    best_data['fields']['name'] = source.get("first_name", 'Noname')
    best_data['fields']['last_name'] = source.get("last_name", 'Nosurname')
    best_data['fields']['age'] = in_age(source.get("bdate", -1))
    best_data['fields']['sex'] = source.get("sex", -1)
    best_data['fields']['relation'] = source.get("relation", -1)
    best_data['fields']['city'] = source.get("city", -1)
    
    photos = dict_.get('photo', None)

    best_photo = {}
    best_photo['model'] = 'photo'
    best_photo['fields'] = []
    for photo in photos:  
        photo_id = photo['id']
        url = max(photo["sizes"], key=lambda x: x['height'] * x['width'])["url"]
        
        best_photo['fields'].append({'photo_id': photo_id, 'url': url})

    return best_data, best_photo