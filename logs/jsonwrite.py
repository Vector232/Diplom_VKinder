import json

def write(f_name, data):
    if not isinstance(data, (dict, list)):
        try:
            data.json()
        except Exception:
            print('Ошибка в преобразовании типа данных!')
            
    with open(f_name, 'w',  encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def read(f_name):
    try:
        with open(f_name, 'r',  encoding='utf-8') as f:
            data = json.load(f)
    except Exception:
        print(f'Не удалость прочесть {f_name}')
        data = []
    return data
