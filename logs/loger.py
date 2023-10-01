from datetime import datetime

class Loger:
    def __init__(self):
        self.start_data = datetime.now()
        with open('temp/log.txt', 'w', encoding='utf-8') as f:
            f.write(f'{self.start_data}: Начало работы.\n')

    def log(self, data):
        self.operive_time = datetime.now() - self.start_data
        with open('temp/log.txt', 'a', encoding='utf-8') as f:
            f.write(f'{self.operive_time}: {data}\n')