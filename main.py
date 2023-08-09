import vk_api
import database.vkinderdb


if __name__ == '__main__':
    print(f'{"НАЧАЛО РАБОТЫ ПРОГРАММЫ":*^31}')

    session = vk_api.VK_session(env=False)
    
    session.start()

    session.test1()
    
