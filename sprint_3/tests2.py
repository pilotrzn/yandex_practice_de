import requests

LOGIN_URL = 'http://158.160.172.156/login/'

if __name__ == '__main__':

    data = {
        'username': 'test_parser_user',
        'password': 'testpassword',
        'csrfmiddlewaretoken': 'token'
    }

    session = requests.session()

    resp = session.get(LOGIN_URL)
    resp_s = resp.text
    resp_x = resp_s.split(' ')

    for a in resp:
        if 'name' in str(a):
            split_str = str(a).split('"')
            name = split_str[0]
            token = split_str[1]
            print(token)

    data['csrfmiddlewaretoken'] = token

    # POST- запрос:
    response = session.post(LOGIN_URL, data=data)
    response.encoding = 'utf-8'

    print(response.text)