# заполняет крточку пользователя
def makeusercard(info: dict, get_photo = False) -> dict:
    def make_user_info(info):
        source = info.get('response')
        if source: source = source[0]
        else: return {}, [], []

        data = {}
        data['model'] = 'user'
        data['fields'] = {}
        data['fields']['user_id'] = source.get("id", None)
        data['fields']['name'] = source.get("first_name", 'Noname')
        data['fields']['last_name'] = source.get("last_name", 'Nosurname')
        data['fields']['bdate'] = source.get("bdate", None)
        data['fields']['sex'] = source.get("sex", None)
        data['fields']['relation'] = source.get("relation", None)
        if source.get("city", None):
            data['fields']['city'] = source['city'].get("title")
        else:
            data['fields']['city'] = None

        return data

    def make_user_photo(info):
        source = info.get('response')[0]
        photos = info.get('photo', [])

        data = []
        for photo in photos:
            best_photo = {}
            best_photo['model'] = 'photo'
            best_photo['fields'] = {}
            best_photo['fields']['user_id'] = source.get("id", None)
            best_photo['fields']['photo_id'] = photo.get('id', None)

            url = max(photo["sizes"], key=lambda x: x['height'] * x['width'])["url"] # подумать о переносе в другое место
            best_photo['fields']['url'] = url

            data.append(best_photo)
        return data
    
    def make_user_noted(info):
        source = info.get('response')[0]
        photos_tags = info.get('was_noted', [])
        if photos_tags != []:
            photos_tags = photos_tags.get('items', [])

        data = []
        for photo_tags in photos_tags:
            photo = {}
            photo['model'] = 'photo_with_user'
            photo['fields'] = {}
            photo['fields']['user_id'] = source.get("id", None) #  ID не владельца фото, а тегнутого пользователя!
            photo['fields']['photo_id'] = photo_tags.get('id', None)
            
            url = max(photo_tags["sizes"], key=lambda x: x['height'] * x['width'])["url"] # подумать о переносе в другое место
            photo['fields']['url'] = url

            data.append(photo)
        return data


    best_data = make_user_info(info)
    
    # если фото не просили, то закругляемся
    if not get_photo: return best_data

    best_photos = make_user_photo(info)
    
    was_noted = make_user_noted(info)
    

    return best_data, best_photos, was_noted