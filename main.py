import vk_api
import usercardmaker as ucm
import database.vkinderdbselect as dbselect
# это нужно будет убрать
from database.vkinderdbmodel import *
from pprint import pprint
if __name__ == '__main__':
    print(f'{"НАЧАЛО РАБОТЫ ПРОГРАММЫ":*^31}')

    session = vk_api.VK_session(test=True)
    
    session.start()

    info = session.get_user_info(session.user_id, get_photo=True)
    
    card, photos, was_noted = ucm.makeusercard(info, get_photo=True)

    # print(card)
    # for photo in photos:
    #     print(photo)
    # print(was_noted)
    db = dbselect.DateBase()
   
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

    candidates = session.find_candidates(db, card)
    # print(candidates)

    print(f'{"КОНЕЦ РАБОТЫ ПРОГРАММЫ":*^31}')

    

    
