# VKINDER - 'Я таки найду тебе пару!'
## Чтобы работало:
1. Нужна папка Temp.
2. Нужен файл .env с содержимым по шаблону:
---- 
- LOGIN = '****@mail.ru'
- PASSWORD = 'VK_password'
- USER_ID = '9******60'
- USER_TOKEN = 'vk1.a.Xjs0o58ocMaLITul-jVax...'
- CLIENT_ID = '51******77'
- APP_TOKEN = 'None'


- dialect = 'postgresql'
- driver = 'psycopg2'
- login_DB = 'postgres'
- password_DB = '********'
- server_name = 'localhost'
- port = '5432'
- db_name = 'VKinderDB'

- card = {'model': 'user', 
                         'user_id': 95135266, 
                         'fields': {'name': 'Владислав', 
                                    'last_name': 'Троян', 
                                    'bdate': '26.3.2000', 
                                    'sex': 2, 'relation': 0, 
                                    'city': 'Симферополь'}}
----
3. Нужна БД с соответствующим именем. Пустой достаточно. Все создаст скрипт. И удалит.


