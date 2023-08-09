import json

def write(f_name, data):
    with open(f_name, 'w',  encoding='utf-8') as f:
        json.dump(data.json(), f, ensure_ascii=False, indent=4)

def read(f_name):
    with open(f_name, 'r',  encoding='utf-8') as f:
        data = json.load(f)
    return data
