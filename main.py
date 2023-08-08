import re

url = 'https://oauth.vk.com/blank.html#access_token=vk1.a.XB4Rvw-k_ihndvzWqBDze_ceRqEu18GrxBER7BKT6NjI9qBWpSZQksVylYcJiDFWqlCjOpe5PAWyF0fVE5IZ48xJsYKTTJ-9YG1t-mFnj8oMDUCkxfVTNgHd2GVb9D6BOBcK1LoyEE6PjxkymfgNFzNTnLGzSP2HimsfjUl9F1Hp11zuOoA0lsBs0LUp97Xs&expires_in=86400&user_id=95135266'
patern = r'.*access_token=(.*)&expires_in.*'
replace  = r'\1'
token = re.sub(patern, replace, url)
print(token)