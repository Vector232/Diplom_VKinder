# заполняет крточку пользователя
from datetime import datetime




def makeusercard(dict_: dict, get_photo = False) -> dict:    
    source = dict_["response"][0]

    best_data = {}
    best_data['model'] = 'user'
    best_data['user_id'] = source.get("id", None)
    best_data['fields'] = {}
    best_data['fields']['name'] = source.get("first_name", 'Noname')
    best_data['fields']['last_name'] = source.get("last_name", 'Nosurname')
    best_data['fields']['age'] = source.get("bdate", None)
    best_data['fields']['sex'] = source.get("sex", None)
    best_data['fields']['relation'] = source.get("relation", None)
    if source.get("city", None):
        best_data['fields']['city'] = source['city'].get("title")
    else:
        best_data['fields']['city'] = None
    
    if not get_photo: return best_data

    photos = dict_.get('photo', None)

    best_photo = {}
    best_photo['model'] = 'photo'
    best_photo['fields'] = []
    for photo in photos:  
        photo_id = photo['id']
        url = max(photo["sizes"], key=lambda x: x['height'] * x['width'])["url"]
        
        best_photo['fields'].append({'photo_id': photo_id, 'url': url})

    return best_data, best_photo