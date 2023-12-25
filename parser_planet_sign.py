import requests
import csv
from bs4 import BeautifulSoup as BS
from parser_natal_chart import city_coords

def request_sign(minute, hour, day, month, year, city):
    latitude, longitude = city_coords(city)
    if latitude == longitude == 1000:
        return False
    city = city.replace(' ', '+')
    req = ("https://geocult.ru/natalnaya-karta-onlayn-raschet?fn=" + "name" + "&fd=" + day + "&fm=" + month + "&fy=" +
           year + "&fh=" + hour + "&fmn=" + minute + "&c1=" + city + "%2C+Россия&ttz=20&tz=Europe%2FMoscow&tm=3&lt=" +
           latitude + "&ln=" + longitude + "&hs=P&sb=1")
    req = requests.get(req)
    html = BS(req.content, 'html.parser')
    element = html.findAll("center")[1].table.find_all('tr')
    result = list()
    planets  ={'Солнце' : 1, 'Луна' : 3, 'Меркурий' : 4, 'Венера' : 5,'Марс' : 6, 'Юпитер' : 7, 'Сатурн' : 8,
               'Уран' : 9, 'Нептун' : 10, 'Плутон' : 11}
    for i in range(1, 8):
        temp = element[i].find_all('td')
        result.append([temp[0].text.split()[1], temp[1].text.split()[1]])
        with open('natal_chart_db.csv', newline='', encoding='utf8') as csvfile:
            read = csv.reader(csvfile, delimiter=';')
            for j in read:
                if j[0] == temp[1].text.split()[1]:
                    result[i - 1].append(j[planets[temp[0].text.split()[1]]])
    return result