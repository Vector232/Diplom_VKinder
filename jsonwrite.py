import json

def write(f_name, data):
    if not isinstance(data, (dict, list)):
        try:
            data.json()
        except:
            print('Ошибка в преобразовании типа данных!')
            
    with open(f_name, 'w',  encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def read(f_name):
    with open(f_name, 'r',  encoding='utf-8') as f:
        data = json.load(f)
    return data
