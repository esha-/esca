#!/usr/bin/python3
'''
This script for searching realtors offers in realty.yandex base
with client parameters
'''
from grab import Grab
import cgi
import html

#BASE_URL = 'https://realty.yandex.ru/search?type=RENT&category=APARTMENT&roomsTotal=2&rentTime=LARGE'

BASE_URL = 'https://realty.yandex.ru/search?'
# Getting parameters from index page
param = {}
form = cgi.FieldStorage()

param['type'] =  html.escape(form.getfirst("type", ''))
param['category'] = html.escape(form.getfirst("category", ''))
param['roomsTotal'] = html.escape(form.getfirst("roomsTotal", ''))
param['metro'] = html.escape(form.getfirst("metro", ""))
param['rgid'] = html.escape(form.getfirst("rgid", ""))  # location/city

param['areaMin'] =  html.escape(form.getfirst("areaMin", "0"))
param['areaMax'] =  html.escape(form.getfirst("areaMax", "1000"))

def price_format(p):
    '''
    Format unicode price string to int
    '40 000 Р в месяц' to '40000' 
    '''
    string = p.split(' ')[0]
    price = ''
    for ch in string:
        try:
            n = int(ch)
            price = price + ch
        except:
            continue
    return int(price)
    
def get_data(url):
    '''
    Getting data(price and offers href) from Yandex Realt with client parameters
    '''
    #print(url)

    price_list = []
    href_list = []

    g = Grab()
    g.go(url)

    # search html class with price
    data_list = g.xpath_list('//*[@class="serp-item__price"]')
    total = 0
    for p in data_list:
        price = price_format(p.text_content())
        total += price
        price_list.append(price)
    
    # search html class with href
    data_list = g.xpath_list('//*[@class="link link_redir_yes stat__click i-bem"]')
    for h in data_list:
        href_list.append(h.get('href'))

    if len(price_list) != 0:
        aver_price = total / len(price_list)
        return aver_price, href_list
    else:
        return 0, []

##############################################################
print("Content-type: text/html\n")
print('''
        <!DOCTYPE HTML>
        <html>
        <head>
          <meta charset="utf-8">
          <title>Калькулятор</title>
          <style>
            body {
              background: #c7b39b url(../images/f2.jpg);
              color: #000080;
            }
        </style>
        </head>
      ''')
url = BASE_URL
# Adding parameters in url string
i = 0
for key in param:
    url += key + '=' + param[key] + '&'
    if param[key] == '' and key != 'metro':  # default metro value is ""
        i = 1
        break
if i == 1:
    print('<h2>Пожалуйста, заполните все параметры</h2>')
else:
    href = []
    aver_price, href = get_data(url)
    if aver_price == 0:
        print ('<h2>По вашему запросу не найдено подходящих предложений</h2>')
    else:
        print('<h2> Средняя cтоимость жилья по вашим параметрам:</h2>' + '<h2>'+ str(aver_price) +'</h2>')
        print('<p>Похожие объявления:</p>')
        for h in href:
             print('<a href="' + h + '" >' + h.replace('//', 'htps://') + '</a><br>')
print('''
    <input type="button" onclick="history.back();" value="Назад"/>
''')
print("""</body>\n</html>""")
