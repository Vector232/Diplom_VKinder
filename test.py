import time
from selenium import webdriver

driver = webdriver.Edge()

driver.maximize_window()

driver.get(f'https://oauth.vk.com/authorize?client_id=51723957&display=page&scope=photos&response_type=token&v=5.131')
time.sleep(5)