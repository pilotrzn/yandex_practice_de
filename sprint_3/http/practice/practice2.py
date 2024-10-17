import requests
from bs4 import BeautifulSoup


LOGIN_URL = 'http://158.160.172.156/login/'
CSCF = {'name': 'csrfmiddlewaretoken'}

data = {
    'username': 'test_parser_user',
    'password': 'testpassword',
}

with requests.session() as session:
    session.cookies.get_dict()
    soup = BeautifulSoup(session.get(LOGIN_URL).text, 'lxml')
    data['csrfmiddlewaretoken'] = soup.find('input', CSCF).get('value')
    response = session.post(url=LOGIN_URL, data=data)
    print(response.status_code)
