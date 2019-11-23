import requests
import config
import telebot
import datetime
from bs4 import BeautifulSoup
from typing import List, Tuple

telebot.apihelper.proxy = {'https': 'https://141.125.82.106:80'}
bot = telebot.TeleBot(config.access_token)
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
dni = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']


def get_page(group, week=''):
    if week:
        week = str(week) + '/'
    if week == '0':
        week = ''
    url = '{domain}/{group}/{week}raspisanie_zanyatiy_{group}.htm'.format(
        domain=config.domain,
        week=week,
        group=group)
    response = requests.get(url)
    web_page = response.text
    return web_page


def parse_schedule(web_page, day):
    soup = BeautifulSoup(web_page, "html5lib")

    # Получаем таблицу с расписанием на понедельник
    schedule_table = soup.find("table", attrs={"id": f"{day}day"})

    if schedule_table == None:
        return None, None, None

    # Время проведения занятий
    times_list = schedule_table.find_all("td", attrs={"class": "time"})
    times_list = [time.span.text for time in times_list]

    # Место проведения занятий
    locations_list = schedule_table.find_all("td", attrs={"class": "room"})
    locations_list = [room.span.text for room in locations_list]

    # Название дисциплин и имена преподавателей
    lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
    lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
    lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]

    return times_list, locations_list, lessons_list


@bot.message_handler(commands=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])
def get_schedule(message):
    """ Получить расписание на указанный день """
    # PUT YOUR CODE HERE
    week = ''
    try:
        day, group, week = message.text.split()
        day = day[1:]
    except ValueError:
        try:
            day, group = message.text.split()
            day = day[1:]
        except ValueError:
            bot.send_message(message.chat.id, 'Wrong input')
            return
    for i in range(len(days)):
        if days[i] == day:
            day = i + 1
    web_page = get_page(group, week)
    times_lst, locations_lst, lessons_lst = \
        parse_schedule(web_page, day)
    resp = ''
    if times_lst != None:
        for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
            resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
    else:
        resp += 'Отдых'
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['near'])
def get_near_lesson(message):
    """ Получить ближайшее занятие """
    # PUT YOUR CODE HERE
    try:
        _, group = message.text.split()
    except ValueError:
        bot.send_message(message.chat.id, 'Wrong input')
        return
    h = datetime.datetime.now().hour
    m = datetime.datetime.now().minute
    day = datetime.date.today().isoweekday()
    instday = day
    week = datetime.date.today().isocalendar()
    week = (week[1] + 1) % 2 + 1
    web_page = get_page(group, week)
    resp = ''
    while resp == '':
        times_lst, locations_lst, lessons_lst = \
            parse_schedule(web_page, day)
        if times_lst == None:
            day += 1
            if day == 8:
                day = 1
                week = week % 2 + 1
                web_page = get_page(group, week)
            if day == instday:
                bot.send_message(message.chat.id, 'Группа не существует')
                return
            continue
        if len(times_lst) > 0:
            for i in range(len(times_lst)):
                time = times_lst[i]
                hour = ''
                mint = ''
                hour += time[0]
                hour += time[1]
                mint += time[3]
                mint += time[4]
                if (h <= int(hour)):
                    if (m <= int(mint)):
                        resp += '<b>{}</b>, {}, {}\n'.format(times_lst[i], locations_lst[i], lessons_lst[i])
                        bot.send_message(message.chat.id, resp, parse_mode='HTML')
                        return
                if instday != day:
                    resp += '<b>{}</b>, {}, {}\n'.format(times_lst[i], locations_lst[i], lessons_lst[i])
                    bot.send_message(message.chat.id, resp, parse_mode='HTML')
                    return
        day += 1
        if day == 8:
            day = 1
            week = week % 2 + 1
            web_page = get_page(group, week)
        if day == instday:
            bot.send_message(message.chat.id, 'Группа не существует')
            return


@bot.message_handler(commands=['tommorow'])
def get_tommorow(message):
    """ Получить расписание на следующий день """
    # PUT YOUR CODE HERE
    try:
        _, group = message.text.split()
    except ValueError:
        bot.send_message(message.chat.id, 'Wrong input')
        return
    day = datetime.date.today().isoweekday() + 1
    week = datetime.date.today().isocalendar()
    week = (week[1] + 1) % 2 + 1
    if day == 8:
        day = 1
    web_page = get_page(group, week)
    times_lst, locations_lst, lessons_lst = \
        parse_schedule(web_page, day)
    resp = ''
    if times_lst != None:
        for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
            resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
    if resp == '':
        resp += 'Отдых'
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['all'])
def get_all_schedule(message):
    """ Получить расписание на всю неделю для указанной группы """
    # PUT YOUR CODE HERE
    week = ''
    try:
        _, group, week = message.text.split()
    except ValueError:
        try:
            _, group = message.text.split()
        except ValueError:
            bot.send_message(message.chat.id, 'Wrong input')
            return
    web_page = get_page(group, week)
    resp = ''
    for i in range(len(days)):
        times_lst, locations_lst, lessons_lst = \
            parse_schedule(web_page, i + 1)
        resp += dni[i]
        resp += '\n\n\n'
        if times_lst != None:
            for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
                resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
        else:
            resp += 'Отдых\n\n\n'
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


if __name__ == '__main__':
    bot.polling(none_stop=True)
