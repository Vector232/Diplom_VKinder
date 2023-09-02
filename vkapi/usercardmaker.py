# заполняет крточку пользователя
def makeusercard(dict_: dict, get_photo = False) -> dict:    
    source = dict_["response"][0]

    best_data = {}
    best_data['model'] = 'user'
    best_data['fields'] = {}
    best_data['fields']['user_id'] = source.get("id", None)
    best_data['fields']['name'] = source.get("first_name", 'Noname')
    best_data['fields']['last_name'] = source.get("last_name", 'Nosurname')
    best_data['fields']['bdate'] = source.get("bdate", None)
    best_data['fields']['sex'] = source.get("sex", None)
    best_data['fields']['relation'] = source.get("relation", None)
    if source.get("city", None):
        best_data['fields']['city'] = source['city'].get("title")
    else:
        best_data['fields']['city'] = None
    
    # если фото не просили, то закругляемся
    if not get_photo: return best_data

    photos = dict_['photo']
    best_photos = []
    for photo in photos:
        best_photo = {}
        best_photo['model'] = 'photo'
        best_photo['fields'] = {}
        best_photo['fields']['user_id'] = source.get("id", None)
        best_photo['fields']['photo_id'] = photo.get('id', None)

        url = max(photo["sizes"], key=lambda x: x['height'] * x['width'])["url"] # подумать о переносе в другое место
        best_photo['fields']['url'] = url

        best_photos.append(best_photo)


    photos_tags = dict_['was_noted'].get('items', [])

    was_noted = []
    for photo_tags in photos_tags:
        photo = {}
        photo['model'] = 'photo_with_user'
        photo['fields'] = {}
        photo['fields']['user_id'] = source.get("id", None) #  ID не владельца фото, а тегнутого пользователя!
        photo['fields']['photo_id'] = photo_tags.get('id', None)
        
        url = max(photo_tags["sizes"], key=lambda x: x['height'] * x['width'])["url"] # подумать о переносе в другое место
        photo['fields']['url'] = url

        was_noted.append(photo)

    return best_data, best_photos, was_noted