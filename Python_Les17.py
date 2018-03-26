import requests
from pprint import pprint
from urllib.parse import urlencode

APP_ID = '7e9131e943db4b9b83d38f26c66091cd'
# PASS = '6de7235d3274476a8ce6a45d267fbaf7'
# CALLBACK = 'https://oauth.yandex.ru/verification_code'
AUTH_URL = 'https://oauth.yandex.ru/authorize'

auth_data = {
    'response_type': 'token',
    'client_id': APP_ID
}


# print('?'.join((AUTH_URL, urlencode(auth_data))))

# TOKEN = 'AQAAAAAJO5yQAATpbgxyGPxY9kGyr7LziLXBQW0'


class YaBase:
    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            'Authorization': 'OAuth {}'.format(self.token)
        }


class YaMetrikaUser(YaBase):

    def get_counters(self):
        headers = self.get_headers()
        response = requests.get('https://api-metrika.yandex.ru/management/v1/counters', headers=headers)

        return [Counter(c['id'], self.token) for c in response.json()['counters']]
        # return response.json()['counters']


class Counter(YaBase):

    def __init__(self, counter_id, token):
        self.counter_id = counter_id
        super().__init__(token)

    # Рабочий вариант, но выполнение происходит дольше
    # def get_metrics(self, metric):
    #     headers = self.get_headers()
    #     params = {
    #         'id': self.counter_id,
    #         'metrics': metric
    #     }
    #     response = requests.get('https://api-metrika.yandex.ru/stat/v1/data', params, headers=headers)
    #     try:
    #         return response.json()['data'][0]['metrics'][0]
    #     except IndexError as e:
    #         return e

    @property
    def visits(self):
        headers = self.get_headers()
        params = {
            'id': self.counter_id,
            'metrics': 'ym:s:visits'
        }
        response = requests.get('https://api-metrika.yandex.ru/stat/v1/data', params, headers=headers)
        try:
            return response.json()['data'][0]['metrics'][0]
        except IndexError as e:
            return e

    @property
    def pageviews(self):
        headers = self.get_headers()
        params = {
            'id': self.counter_id,
            'metrics': 'ym:s:pageviews'
        }
        response = requests.get('https://api-metrika.yandex.ru/stat/v1/data', params, headers=headers)
        try:
            return response.json()['data'][0]['metrics'][0]
        except IndexError as e:
            return e

    @property
    def users(self):
        headers = self.get_headers()
        params = {
            'id': self.counter_id,
            'metrics': 'ym:s:users'
        }
        response = requests.get('https://api-metrika.yandex.ru/stat/v1/data', params, headers=headers)
        try:
            return response.json()['data'][0]['metrics'][0]
        except IndexError as e:
            return e


first_user = YaMetrikaUser('AQAAAAAJO5yQAATpbgxyGPxY9kGyr7LziLXBQW0')
counters = first_user.get_counters()
for counter in counters:
    print(counter.counter_id)

    # Вывод результатов с помощью get_metrics:
    # print('Визитов:', counter.get_metrics('ym:s:visits'))
    # print('Просмотров:', counter.get_metrics('ym:s:pageviews'))
    # print('Пользователей:', counter.get_metrics('ym:s:users'))

    print('Визитов:', counter.visits)
    print('Просмотров:', counter.pageviews)
    print('Пользователей:', counter.users)
