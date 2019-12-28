import datetime as dt
from statistics import median
from typing import Optional

from api import get_friends
from api_models import User


def age_predict(user_id: int) -> Optional[float]:
    """ Наивный прогноз возраста по возрасту друзей

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: идентификатор пользователя
    :return: медианный возраст пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    FrList = get_friends(user_id, 'bdate')
    y = ''
    sum = 0
    sumcoun = 0
    DotCount = 0
    for i in range(FrList['response']['count']):
        try:
            dt = FrList['response']['items'][i]['bdate']
        except:
            continue
        for j in range(len(dt)):
            if (dt[j]=='.'):
                DotCount+=1
        if (DotCount==2):
            DotCount=0
            for j in range(len(dt)):
                if DotCount!=2:
                    if(dt[j]=='.'):
                        DotCount+=1
                else:
                    y += dt[j]
        else:
            DotCount = 0
            continue
        sum += int(y)
        sumcoun += 1
        y = ''
        DotCount = 0
    if(sumcoun!=0):
        return 2019 - sum/sumcoun
    else:
        return "No friends?"
