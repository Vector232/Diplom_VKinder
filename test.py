import requests
import os
from pprint import pprint
from dotenv import load_dotenv
load_dotenv()


url = 'https://api.vk.com/method/photos.getUserPhotos'
params = {'access_token': os.getenv('USER_TOKEN'), 
                    'v': 5.131,
                    'user_id': '95135266',
                    'count': 50,
                    'offset': 0
                    }


req = requests.get(url=url, params=params).json()
for note in req['response']['items']:
        pprint(note)