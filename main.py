import vk_api
import database.vkinderdb


if __name__ == '__main__':
    print(f'{"НАЧАЛО РАБОТЫ ПРОГРАММЫ":*^31}')

    session = vk_api.VK_session(env=True)
    
    session.start()

    # session.create_user_card(session.user_id, get_photo=True)

    print(f'{"КОНЕЦ РАБОТЫ ПРОГРАММЫ":*^31}')

    

    
