import requests
from bs4 import BeautifulSoup as BS

def request_compatibility(day, month, year, day2, month2, year2, gender):
    if gender == 'female' :
        req = ("https://my-calend.ru/sovmestimost-po-date-rozhdeniya/" +
               str(day) + "." + str(month) + "." + str(year) + "/" + str(day2) + "." + str(month2) + "." + str(year2))
    else :
        req = ("https://my-calend.ru/sovmestimost-po-date-rozhdeniya/" +
               str(day2) + "." + str(month2) + "." + str(year2) + "/" + str(day) + "." + str(month) + "." + str(year))
    req = requests.get(req)
    html = BS(req.content, 'html.parser')
    elements = html.find_all('div', attrs = {'class' : 'sovmestimost-po-date-rozhdeniya-amount-number'})
    res = (f"Совместимость в любви и браке: {elements[0].text}\nСовместимость в дружбе: "
           f"{elements[1].text}\nСовместимость в работе: {elements[2].text}")
    return res

