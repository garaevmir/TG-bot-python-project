import requests
from bs4 import BeautifulSoup as BS


def request_ru_today_horoscope(sign_today):
    req = requests.get("https://1001goroskop.ru/?znak=" + sign_today)
    html = BS(req.content, 'html.parser')
    element = html.find('div', attrs={'itemprop': 'description'})
    return element.p.text


def request_ru_tomorrow_horoscope(sign_week):
    req = requests.get("https://1001goroskop.ru/?znak=" + sign_week + "&kn=tomorrow")
    html = BS(req.content, 'html.parser')
    element = html.find('div', attrs={'itemprop': 'description'})
    return element.p.text


def request_ru_week_horoscope(sign_week):
    req = requests.get("https://1001goroskop.ru/?znak=" + sign_week + "&kn=week")
    html = BS(req.content, 'html.parser')
    element = html.find('div', attrs={'itemprop': 'description'})
    output = ""
    for i in element:
        output += i.get_text() + '\n'
    return output


def request_horoscope(sign_req, time_period):
    if time_period == 'today':
        return request_ru_today_horoscope(sign_req)
    elif time_period == 'tomorrow':
        return request_ru_tomorrow_horoscope(sign_req)
    elif time_period == 'week':
        return request_ru_week_horoscope(sign_req)
    else:
        return "Доступен только гороскоп на сегодня, завтра или на неделю вперёд."


sign = input()
period = input()
print(request_horoscope(sign, period))
