# Задача:
# Выберите одну или несколько сторонних библиотек Python, например, requests, pandas, numpy, matplotlib,
# pillow.
# После выбора библиотек(-и) изучите документацию к ней(ним), ознакомьтесь с их основными возможностями
# и функциями. К каждой библиотеке дана ссылка на документацию ниже.
# Если вы выбрали:
# requests - запросить данные с сайта и вывести их в консоль.
# pandas - считать данные из файла, выполнить простой анализ данных (на своё усмотрение) и вывести
# результаты в консоль.
# numpy - создать массив чисел, выполнить математические операции с массивом и вывести результаты в консоль.
# matplotlib - визуализировать данные с помощью библиотеки любым удобным для вас инструментом из библиотеки.
# pillow - обработать изображение, например, изменить его размер, применить эффекты и сохранить в другой
# формат.
# В приложении к ссылке на GitHub напишите комментарий о возможностях, которые предоставила вам выбранная
# библиотека и как вы расширили возможности Python с её помощью.

import requests
import pandas
import matplotlib.pyplot as plt

from pprint import pprint

URL = 'https://www.cbr-xml-daily.ru/daily_json.js'
# 'https://urban-university.ru/profile/course?alias=course999421818026'
# URL2 = 'https://urban-university.ru/profile/course'
# URL3 = 'https://yandex.ru/search/?text=python+работа+с+библиотекой+json&lr=10&clid=2261451&win=531'

"""
Использование модуля requests.
Получить данные о курсах валют с сайта на текущую дату и записать 
полученные данные в переменную r в формате json.
"""

r = requests.get(URL)
json_flag = False
if r.ok:
    try:
        r = r.json()
        with open('val.json', 'w', encoding='utf-8') as file:
            file.write(str(r['Valute']))
        # csv_ = pandas.read_json(URL)
        # # csv_2 = pandas.read_json('./val.json')
    except requests.exceptions.JSONDecodeError as e:
        print('Содержимое ответа не в формате json.', 'От источника был получен следующий ответ:',
              r, sep='\n')
    else:
        json_flag = True
pprint(r['Valute'])

"""
Использование модуля pandas.
Сохранить полученные курсы валют в файле .xlsx.
"""

if json_flag:
    # Формируем список валют для записи в файл
    field_list = ['CharCode', 'NumCode', 'Name', 'Nominal', 'Value']
    val_list = []
    for i in r['Valute']:
        line_ = []
        for j in field_list:
            line_.append(r['Valute'][i][j])
        val_list.append(line_)

    val_list.sort(key=lambda x: -x[3])
    pprint(val_list)

    # Сохраняем полученные данные в файл .xlsx
    df1 = pandas.DataFrame(val_list, columns=field_list)
    with pandas.ExcelWriter(f"val_{r['Date'][0:10]}.xlsx") as writer:
        df1.to_excel(writer, sheet_name=str(r['Date'][0:10]))

"""
Использование модуля matplotlib.
Зачитать данные из файла .xlsx, построить график на основе этих данных.
"""

if json_flag:
    chart_data = pandas.read_excel(f"val_{r['Date'][0:10]}.xlsx")
    pprint(chart_data)
    csv_ = chart_data.to_csv()
    print(csv_)
    with open('val.csv', 'w', encoding='utf-8') as file:
        file.write(csv_)
    fig, ax = plt.subplots()

    ax.set_title('Курсы валют')
    ax.set_xlabel('Коды валют')
    ax.set_ylabel('Курс')
    # Если бы мы проводили какой-то реальный анализ диаграммы, то в строке ниже стоило бы c и s взять как
    # обратную величину, умноженную на 10_000, т.е. записать s=10_000/chart_data['Nominal'], но это будет
    # выглядеть не очень красиво на диаграмме, поэтому для наглядности и красоты картинки строчка ниже
    # пусть останется такой, так тоже можно объяснить большие круги, как "нужно взять очень много той валюты,
    # чтобы обменять ее по указанному курсу на рубли:
    ax.scatter(chart_data['NumCode'], chart_data['Value'], c=chart_data['Nominal'], s=chart_data['Nominal'],
               alpha=0.5, cmap='flag')

    # chart_data['Value'].plot()
    plt.show()
