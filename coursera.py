import requests
from requests.auth import HTTPBasicAuth


with requests.Session() as c:
    url = 'https://accounts.coursera.org/signin'
    EMAIL = 'yangdai713@aim.com'
    PASSWORD = 'gofpdseorkg713'
    c.get(url)
    csrftoken = c.cookies[name='csrftoken']
    login_data = dict(EMAIL=EMAIL, PASSWORD=PASSWORD)
    c.post(url, data=login_data, headers={"Referer": "http://www.coursera.org/"})
    page = c.get('http://www.coursera.org/learn/convolutional-neural-network/home/welcome')
    print(page.text)
