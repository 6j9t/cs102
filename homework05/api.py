import requests
import time

import config
import random

def get(url, params={}, timeout=5, max_retries=5, backoff_factor=0.3):
    """ Выполнить GET-запрос

    :param url: адрес, на который необходимо выполнить запрос
    :param params: параметры запроса
    :param timeout: максимальное время ожидания ответа от сервера
    :param max_retries: максимальное число повторных запросов
    :param backoff_factor: коэффициент экспоненциального нарастания задержки
    """
    # PUT YOUR CODE HERE
    jitter = 0.1
    maxdelay = 5
    mindelay = 0.1
    delay = mindelay
    for i in range (max_retries):
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            return response
        else:
            time.sleep(delay)
            delay = min(delay*backoff_factor, maxdelay)
            delay = delay + random.randint(0, 5) * jitter
    return response.raise_for_status()

def get_friends(user_id, fields):
    """ Вернуть данных о друзьях пользователя

    :param user_id: идентификатор пользователя, список друзей которого нужно получить
    :param fields: список полей, которые нужно получить для каждого пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"
    query = f"{config.domain}/friends.get?access_token={config.access_token}&user_id={user_id}&fields={fields}&v={config.v}"
    response = get(query)
    return response.json()

def get_profileinfo(user_id):
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    query = f"{config.domain}/users.get?access_token={config.access_token}&user_id={user_id}&v={config.v}"
    response = get(query)
    return response.json()

def messages_get_history(user_id, offset=0, count=20):
    """ Получить историю переписки с указанным пользователем

    :param user_id: идентификатор пользователя, с которым нужно получить историю переписки
    :param offset: смещение в истории переписки
    :param count: число сообщений, которое нужно получить
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    assert isinstance(offset, int), "offset must be positive integer"
    assert offset >= 0, "user_id must be positive integer"
    assert count >= 0, "user_id must be positive integer"
    # PUT YOUR CODE HERE
