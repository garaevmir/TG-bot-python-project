import requests
import csv
from bs4 import BeautifulSoup as BS

def city_coords(city):
    with open('cities.csv', newline='', encoding='utf8') as csvfile:
        read = csv.reader(csvfile, delimiter=',')
        long, alt = '', ''
        for i in read:
            if i[6].lower() == city.lower():
                return i[17], i[18]
            if i[6] == '':
                if i[2].lower() == city.lower():
                    return i[17], i[18]
        return 1000, 1000


def request_map(minute, hour, day, month, year, city):
    latitude, longitude = city_coords(city)
    if latitude == longitude == 1000:
        return False
    city = city.replace(' ', '+')
    req = ("https://geocult.ru/natalnaya-karta-onlayn-raschet?fn=" + "name" + "&fd=" + day + "&fm=" + month + "&fy=" +
           year + "&fh=" + hour + "&fmn=" + minute + "&c1=" + city + "%2C+Россия&ttz=20&tz=Europe%2FMoscow&tm=3&lt=" +
           latitude + "&ln=" + longitude + "&hs=P&sb=1")
    req = requests.get(req)
    html = BS(req.content, 'html.parser')
    element = html.find('center').a['href']
    return element

print(request_map('0', '11', '8', '5', '2004', 'набережные челны').replace(' ', '%20'))