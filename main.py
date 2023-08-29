import vk_api
import usercardmaker as ucm
import database.vkinderdbselect as dbselect
# это нужно будет убрать
from database.vkinderdbmodel import *

if __name__ == '__main__':
    print(f'{"НАЧАЛО РАБОТЫ ПРОГРАММЫ":*^31}')

    session = vk_api.VK_session(test=True)
    
    session.start()

    info = session.get_user_info(session.user_id, get_photo=True)
    
    card, photos = ucm.makeusercard(info, get_photo=True)
    # print(card)
    # print(photos)
    DB = dbselect.DateBase()
   
    DB.push_user_card(card)
    DB.push_photos(photos, card['user_id'])

    # q = DB.session.query(User)
    # for i in q:
    #     print(i)

    # q = DB.session.query(Photo)
    # for i in q:
    #     print(i)

    candidates = session.find_candidates(DB, card)
    # print(candidates)

    print(f'{"КОНЕЦ РАБОТЫ ПРОГРАММЫ":*^31}')

    

    
